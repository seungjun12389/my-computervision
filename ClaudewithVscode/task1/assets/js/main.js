/**
 * main.js — 렌더링 + 인터랙션
 * Design system: Figma marketing canvas (monochrome chrome + color blocks)
 */
(function () {
  'use strict';

  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  /** XSS 방지를 위한 이스케이프 */
  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function bullets(points) {
    return (
      '<ul class="bullets">' +
      points.map((p) => '<li>' + esc(p) + '</li>').join('') +
      '</ul>'
    );
  }

  /** 칩. mono=true 면 figmaMono 대문자 taxonomy 칩 */
  function tags(items, mono) {
    const cls = mono ? 'tag tag-mono' : 'tag';
    return (
      '<div class="tag-list">' +
      items.map((i) => '<span class="' + cls + '">' + esc(i) + '</span>').join('') +
      '</div>'
    );
  }

  const COPY_ICON =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h8"/></svg>';

  const ARROW_ICON =
    '<svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>';

  /* ======================================================================
     렌더링
     ====================================================================== */

  function renderHero(data) {
    $('#heroEyebrow').textContent = data.profile.eyebrow;
    $('#heroName').textContent = data.profile.name;
    $('#heroTagline').textContent = data.profile.tagline;

    // 네비 / 히어로의 GitHub CTA 는 같은 주소를 공유한다
    ['#heroGithub', '#navGithub', '#navGithubMobile'].forEach((sel) => {
      const el = $(sel);
      if (el) el.href = data.contact.github;
    });
  }

  /** 검은 마퀴 스트립 — 끊김 없는 순환을 위해 목록을 두 번 렌더한다 */
  function renderMarquee(data) {
    const items = data.marquee
      .map((m) => '<span class="marquee-item">' + esc(m) + '</span>')
      .join('');
    $('#marqueeTrack').innerHTML = items + items;
  }

  function renderAbout(data) {
    const { about, highlights } = data.profile;
    // 긴 키워드부터 치환해야 부분 매칭 문제가 없다
    const words = highlights.slice().sort((a, b) => b.length - a.length);

    $('#aboutBody').innerHTML = about
      .map((para) => {
        let text = esc(para);
        words.forEach((w) => {
          const safe = esc(w).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          text = text.replace(
            new RegExp('(?![^<]*>)' + safe, 'g'),
            '<mark>' + esc(w) + '</mark>'
          );
        });
        return '<p class="reveal">' + text + '</p>';
      })
      .join('');
  }

  function renderEducation(data) {
    const e = data.education;
    $('#educationBody').innerHTML =
      '<p class="eyebrow">02 — EDUCATION</p>' +
      '<div class="edu-head">' +
      '<div>' +
      '<h2 class="block-title">' + esc(e.school) + '</h2>' +
      '<p class="edu-major">' + esc(e.major) + '</p>' +
      '</div>' +
      '<p class="edu-period">' + esc(e.period) + '</p>' +
      '</div>' +
      '<ul class="edu-details">' +
      e.details.map((d) => '<li>' + esc(d) + '</li>').join('') +
      '</ul>' +
      '<p class="caption edu-courses-label">RELATED COURSEWORK</p>' +
      tags(e.courses);
  }

  function renderActivities(data) {
    $('#activitiesList').innerHTML = data.activities
      .map(
        (a) =>
          '<li class="timeline-item reveal">' +
          '<div class="timeline-meta">' +
          '<span class="caption">' + esc(a.period) + '</span>' +
          '<span class="timeline-org">' + esc(a.org) + '</span>' +
          '</div>' +
          '<div>' +
          '<h3 class="timeline-title">' + esc(a.title) + '</h3>' +
          bullets(a.points) +
          '</div>' +
          '</li>'
      )
      .join('');
  }

  function renderSkills(data) {
    $('#skillsGrid').innerHTML = data.skills
      .map(
        (s) =>
          '<div class="skill-group">' +
          '<h3 class="skill-category">' + esc(s.category) + '</h3>' +
          tags(s.items) +
          '</div>'
      )
      .join('');
  }

  function renderProjects(data) {
    $('#projectGrid').innerHTML = data.projects
      .map(
        (p) =>
          '<article class="project-card reveal">' +
          '<div class="project-meta">' +
          '<span class="project-period">' + esc(p.period) + '</span>' +
          '<span class="project-type">' + esc(p.type) + '</span>' +
          '</div>' +
          '<h3 class="project-name">' + esc(p.name) + '</h3>' +
          '<p class="project-summary">' + esc(p.summary) + '</p>' +
          bullets(p.points) +
          '<p class="caption project-stack-label">TECH STACK</p>' +
          tags(p.stack, true) +
          '<div class="project-footer">' +
          '<a class="btn btn-secondary" href="' + esc(p.github) + '" target="_blank" rel="noopener noreferrer" ' +
          'aria-label="' + esc(p.name) + ' GitHub 저장소 (새 창)">' +
          'GitHub 저장소' + ARROW_ICON +
          '</a>' +
          '</div>' +
          '</article>'
      )
      .join('');
  }

  function renderPromo(data) {
    const email = data.contact.emailUser + '@' + data.contact.emailDomain;
    $('#promoBanner').innerHTML =
      '<p class="promo-text">' + esc(data.promo.text) + '</p>' +
      '<a class="btn btn-magenta" href="mailto:' + esc(email) + '?subject=' +
      encodeURIComponent('[포트폴리오] 이력서 요청') + '">' +
      esc(data.promo.cta) + '</a>';
  }

  function renderContact(data, config) {
    const c = data.contact;
    // 스팸 봇 수집 방지를 위해 런타임에 조합
    const email = c.emailUser + '@' + c.emailDomain;
    const cards = [];

    cards.push(
      '<article class="contact-card">' +
      '<p class="caption contact-label">GITHUB</p>' +
      '<a class="contact-value" href="' + esc(c.github) + '" target="_blank" rel="noopener noreferrer">' +
      esc(c.github.replace('https://', '')) + '</a>' +
      '<button class="copy-btn" type="button" data-copy="' + esc(c.github) + '" aria-label="GitHub 주소 복사">' +
      COPY_ICON + 'COPY' +
      '</button>' +
      '</article>'
    );

    cards.push(
      '<article class="contact-card">' +
      '<p class="caption contact-label">E-MAIL</p>' +
      '<a class="contact-value" href="mailto:' + esc(email) + '">' + esc(email) + '</a>' +
      '<button class="copy-btn" type="button" data-copy="' + esc(email) + '" aria-label="이메일 주소 복사">' +
      COPY_ICON + 'COPY' +
      '</button>' +
      '</article>'
    );

    if (config.showPhone) {
      cards.push(
        '<article class="contact-card">' +
        '<p class="caption contact-label">PHONE</p>' +
        '<a class="contact-value" href="tel:' + esc(c.phone.replace(/-/g, '')) + '">' + esc(c.phone) + '</a>' +
        '<button class="copy-btn" type="button" data-copy="' + esc(c.phone) + '" aria-label="전화번호 복사">' +
        COPY_ICON + 'COPY' +
        '</button>' +
        '</article>'
      );
    }

    $('#contactGrid').innerHTML = cards.join('');
  }

  function renderFooter(data) {
    const c = data.contact;
    const email = c.emailUser + '@' + c.emailDomain;

    const columns = data.footerColumns.concat([
      {
        heading: 'CONTACT',
        links: [
          { label: 'GitHub', href: c.github, external: true },
          { label: 'E-mail', href: 'mailto:' + email },
        ].concat(
          SITE_CONFIG.showPhone
            ? [{ label: 'Phone', href: 'tel:' + c.phone.replace(/-/g, '') }]
            : []
        ),
      },
    ]);

    $('#footerGrid').innerHTML = columns
      .map(
        (col) =>
          '<div>' +
          '<p class="caption footer-col-head">' + esc(col.heading) + '</p>' +
          '<ul class="footer-links">' +
          col.links
            .map(
              (l) =>
                '<li><a href="' + esc(l.href) + '"' +
                (l.external ? ' target="_blank" rel="noopener noreferrer"' : '') +
                '>' + esc(l.label) + '</a></li>'
            )
            .join('') +
          '</ul>' +
          '</div>'
      )
      .join('');
  }

  /* ======================================================================
     인터랙션
     ====================================================================== */

  /** 스크롤 시 nav 하단 헤어라인 */
  function initNavScroll() {
    const nav = $('#topNav');
    const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 8);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /** 햄버거 오버레이 (960px 이하) */
  function initMobileNav() {
    const btn = $('#menuToggle');
    const nav = $('#nav');

    function setOpen(open) {
      nav.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
      document.body.style.overflow = open ? 'hidden' : '';
    }

    btn.addEventListener('click', () => {
      setOpen(btn.getAttribute('aria-expanded') !== 'true');
    });
    $$('#nav a').forEach((a) => a.addEventListener('click', () => setOpen(false)));

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        btn.focus();
      }
    });

    window.matchMedia('(min-width: 961px)').addEventListener('change', (e) => {
      if (e.matches) setOpen(false);
    });
  }

  /** 현재 섹션 메뉴 활성화 — scroll-spy */
  function initScrollSpy() {
    const links = $$('#navList .nav-link');
    const map = new Map();
    links.forEach((link) => {
      const section = document.querySelector(link.getAttribute('href'));
      if (section) map.set(section, link);
    });
    if (!map.size) return;

    const visible = new Set();

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) visible.add(entry.target);
          else visible.delete(entry.target);
        });
        const current = Array.from(map.keys()).find((s) => visible.has(s));
        links.forEach((l) => l.classList.remove('is-active'));
        if (current) map.get(current).classList.add('is-active');
      },
      { rootMargin: '-30% 0px -55% 0px', threshold: 0 }
    );

    map.forEach((_, section) => observer.observe(section));
  }

  /** 클립보드 복사 + 토스트 */
  function initCopy() {
    const toast = $('#toast');
    let timer = null;

    function showToast(message) {
      toast.textContent = message;
      toast.classList.add('is-visible');
      clearTimeout(timer);
      timer = setTimeout(() => toast.classList.remove('is-visible'), 2000);
    }

    async function copy(text) {
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(text);
          return true;
        }
      } catch (e) {
        /* 아래 폴백으로 진행 */
      }
      // file:// 이나 구형 브라우저용 폴백
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      let ok = false;
      try {
        ok = document.execCommand('copy');
      } catch (e) {
        ok = false;
      }
      document.body.removeChild(ta);
      return ok;
    }

    document.addEventListener('click', async (e) => {
      const btn = e.target.closest('[data-copy]');
      if (!btn) return;
      const ok = await copy(btn.dataset.copy);
      showToast(ok ? '복사되었습니다' : '복사에 실패했습니다');
    });
  }

  /** 스크롤 진입 리빌 */
  function initReveal() {
    const items = $$('.reveal');
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (reduce || !('IntersectionObserver' in window)) {
      items.forEach((el) => el.classList.add('is-visible'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry, i) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          el.style.transitionDelay = Math.min(i, 4) * 60 + 'ms';
          el.classList.add('is-visible');
          obs.unobserve(el);
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );

    items.forEach((el) => observer.observe(el));
  }

  /* ======================================================================
     초기화
     ====================================================================== */
  document.addEventListener('DOMContentLoaded', () => {
    if (typeof RESUME === 'undefined') {
      console.error('data.js 를 불러오지 못했습니다.');
      return;
    }

    renderHero(RESUME);
    renderMarquee(RESUME);
    renderAbout(RESUME);
    renderEducation(RESUME);
    renderActivities(RESUME);
    renderSkills(RESUME);
    renderProjects(RESUME);
    renderPromo(RESUME);
    renderContact(RESUME, SITE_CONFIG);
    renderFooter(RESUME);

    $('#year').textContent = new Date().getFullYear();

    initNavScroll();
    initMobileNav();
    initScrollSpy();
    initCopy();
    initReveal(); // 동적 렌더링 이후에 관찰해야 한다
  });
})();
