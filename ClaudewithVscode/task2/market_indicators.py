"""
주요 시장 지표 조회 스크립트 (Yahoo Finance)

조회 대상:
    - S&P 500, 나스닥 종합, 다우존스 산업평균
    - 코스피, 코스닥
    - 미국채 10년물 금리
    - 금 선물 가격
    - 원/달러 환율

사용법:
    python market_indicators.py                  # 표 형태로 출력
    python market_indicators.py --json           # JSON 출력
    python market_indicators.py --csv out.csv    # CSV 파일로 저장
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import unicodedata
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

try:
    import yfinance as yf
except ImportError:
    sys.exit("yfinance 가 설치되어 있지 않습니다. 먼저 실행하세요:\n\n    pip install yfinance\n")


@dataclass(frozen=True)
class Indicator:
    """조회할 지표의 정의."""

    name: str          # 화면에 표시할 이름
    ticker: str        # Yahoo Finance 티커
    unit: str          # 단위 (pt, %, USD, KRW ...)
    decimals: int = 2  # 소수점 자릿수


INDICATORS: list[Indicator] = [
    Indicator("S&P 500", "^GSPC", "pt"),
    Indicator("나스닥 종합", "^IXIC", "pt"),
    Indicator("다우존스", "^DJI", "pt"),
    Indicator("코스피", "^KS11", "pt"),
    Indicator("코스닥", "^KQ11", "pt"),
    Indicator("미국채 10년물", "^TNX", "%", decimals=3),
    Indicator("금 (COMEX 선물)", "GC=F", "USD/oz"),
    Indicator("원/달러 환율", "KRW=X", "KRW", decimals=2),
]


@dataclass
class Quote:
    """지표 1건의 조회 결과."""

    name: str
    ticker: str
    unit: str
    last: Optional[float]
    previous_close: Optional[float]
    change: Optional[float]
    change_pct: Optional[float]
    as_of: Optional[str]
    error: Optional[str] = None


REQUEST_TIMEOUT = 15  # 초. 응답이 없을 때 무한정 매달리지 않도록 제한
MAX_ATTEMPTS = 3      # 일시적 네트워크 오류에 대한 재시도 횟수
RETRY_BACKOFF = 1.5   # 재시도 간 대기 시간(초), 시도마다 배로 증가


def fetch_quote(ind: Indicator, period: str = "1mo") -> Quote:
    """단일 지표를 Yahoo Finance 에서 조회한다.

    최근 영업일 종가와 그 직전 영업일 종가를 비교해 등락을 계산한다.
    휴장일/데이터 지연을 감안해 넉넉한 기간(period)을 받아 마지막 2개 행만 사용한다.

    Yahoo 쪽 응답 실패나 연결 끊김은 일시적인 경우가 많으므로 MAX_ATTEMPTS 만큼
    재시도한다. KeyboardInterrupt(Ctrl+C)는 잡지 않고 그대로 올려보내
    main() 에서 조용히 종료되게 한다.

    yfinance 는 버전에 따라 조회 실패를 예외로 던지기도, 빈 DataFrame 으로
    돌려주기도 한다. 두 경우 모두 재시도한 뒤 최종 실패로 처리한다.
    """
    last_error = "알 수 없는 오류"

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            hist = yf.Ticker(ind.ticker).history(
                period=period, auto_adjust=False, timeout=REQUEST_TIMEOUT
            )
            hist = hist.dropna(subset=["Close"])

            if hist.empty:
                # yfinance 는 조회 실패를 예외 대신 빈 DataFrame 으로 돌려주기도 한다.
                # 일시적 실패와 구분이 안 되므로 빈 결과도 재시도 대상으로 본다.
                last_error = "데이터 없음 (빈 응답)"
                if attempt < MAX_ATTEMPTS:
                    time.sleep(RETRY_BACKOFF * attempt)
                continue

            last = float(hist["Close"].iloc[-1])
            prev = float(hist["Close"].iloc[-2]) if len(hist) >= 2 else None
            change = last - prev if prev is not None else None
            change_pct = (change / prev * 100) if prev not in (None, 0) else None
            as_of = hist.index[-1].strftime("%Y-%m-%d")

            return Quote(ind.name, ind.ticker, ind.unit, last, prev, change, change_pct, as_of)

        except KeyboardInterrupt:
            raise

        except BaseException as exc:
            # curl_cffi 는 콜백 안에서 난 오류를 Exception 이 아닌 형태로 다시 던지는
            # 경우가 있어(연결 중단 등) BaseException 까지 받아낸다.
            last_error = f"{type(exc).__name__}: {exc}".strip().splitlines()[0][:120]
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_BACKOFF * attempt)

    return Quote(ind.name, ind.ticker, ind.unit, None, None, None, None, None,
                 error=f"{MAX_ATTEMPTS}회 시도 실패 - {last_error}")


def fetch_all() -> list[Quote]:
    return [fetch_quote(ind) for ind in INDICATORS]


def _width(text: str) -> int:
    """한글/한자 등 전각 문자를 2칸으로 계산한 표시 폭."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)


def _pad(text: str, width: int, align: str = "<") -> str:
    """표시 폭 기준 정렬 (한글 포함 문자열에서 str.ljust 대신 사용)."""
    space = " " * max(0, width - _width(text))
    return text + space if align == "<" else space + text


def _fmt(value: Optional[float], decimals: int, signed: bool = False) -> str:
    if value is None:
        return "-"
    return f"{value:+,.{decimals}f}" if signed else f"{value:,.{decimals}f}"


def print_table(quotes: list[Quote]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = "=" * 92

    print(f"\n주요 시장 지표  (조회 시각: {now})")
    print(line)
    print(
        _pad("지표", 20) + _pad("티커", 10)
        + _pad("현재값", 16, ">") + _pad("전일대비", 14, ">")
        + _pad("등락률", 12, ">") + _pad("기준일", 14, ">")
    )
    print("-" * 92)

    for q, ind in zip(quotes, INDICATORS):
        if q.error:
            print(_pad(q.name, 20) + _pad(q.ticker, 10) + f"조회 실패: {q.error}")
            continue

        pct = "-" if q.change_pct is None else f"{q.change_pct:+.2f}%"
        print(
            _pad(q.name, 20) + _pad(q.ticker, 10)
            + _pad(_fmt(q.last, ind.decimals), 16, ">")
            + _pad(_fmt(q.change, ind.decimals, signed=True), 14, ">")
            + _pad(pct, 12, ">")
            + _pad(q.as_of or "-", 14, ">")
        )

    print("-" * 92)
    print("단위: 지수=pt, 미국채 10년물=%, 금=USD/oz, 원달러=KRW")
    print("출처: Yahoo Finance (종가 기준, 실시간 시세와 차이가 있을 수 있음)\n")


def to_json(quotes: list[Quote]) -> str:
    payload = {
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "source": "Yahoo Finance",
        "indicators": [asdict(q) for q in quotes],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def to_csv(quotes: list[Quote], path: str) -> None:
    import csv

    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["지표", "티커", "단위", "현재값", "전일종가", "전일대비", "등락률(%)", "기준일", "비고"])
        for q in quotes:
            writer.writerow([
                q.name, q.ticker, q.unit,
                q.last, q.previous_close, q.change,
                None if q.change_pct is None else round(q.change_pct, 4),
                q.as_of, q.error or "",
            ])


def main() -> int:
    # Windows 콘솔(cp949)에서 한글이 깨지지 않도록 UTF-8 출력으로 강제
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    parser = argparse.ArgumentParser(description="Yahoo Finance 주요 시장 지표 조회")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    parser.add_argument("--csv", metavar="PATH", help="결과를 CSV 파일로 저장")
    args = parser.parse_args()

    try:
        quotes = fetch_all()
    except KeyboardInterrupt:
        print("\n조회를 중단했습니다.", file=sys.stderr)
        return 130

    if args.json:
        print(to_json(quotes))
    else:
        print_table(quotes)

    if args.csv:
        to_csv(quotes, args.csv)
        print(f"CSV 저장 완료: {args.csv}")

    return 0 if any(q.error is None for q in quotes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
