const chapters = [...document.querySelectorAll('.spread[data-chapter]')];
const chapterLinks = [...document.querySelectorAll('[data-chapter-link]')];
const book = document.querySelector('#book');
const previousButton = document.querySelector('#prev-page');
const nextButton = document.querySelector('#next-page');
const currentChapter = document.querySelector('#current-chapter');
const chapterCount = document.querySelector('#chapter-count');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const narrowScreen = window.matchMedia('(max-width: 850px)');
let activeIndex = 0;
let turnTimer;
let enterTimer;

function chapterIndexFromHash() {
  const key = decodeURIComponent(window.location.hash.slice(1));
  return chapters.findIndex((chapter) => chapter.dataset.chapter === key);
}

function renderChapter(index) {
  const focusWasInside = chapters[activeIndex]?.contains(document.activeElement);
  activeIndex = index;
  chapters.forEach((chapter, position) => {
    const active = position === index;
    chapter.classList.toggle('is-active', active);
    chapter.setAttribute('aria-hidden', String(!active));
    chapter.inert = !active;
  });
  chapterLinks.forEach((link) => {
    if (link.dataset.chapterLink === chapters[index].dataset.chapter) {
      link.setAttribute('aria-current', 'page');
    } else {
      link.removeAttribute('aria-current');
    }
  });
  previousButton.disabled = index === 0;
  nextButton.disabled = index === chapters.length - 1;
  currentChapter.textContent = chapters[index].dataset.chapter.toUpperCase();
  chapterCount.textContent = `${String(index).padStart(2, '0')} / ${String(chapters.length - 1).padStart(2, '0')}`;
  document.title = `Katrin Merfeld — ${chapters[index].dataset.chapter[0].toUpperCase()}${chapters[index].dataset.chapter.slice(1)}`;
  if (focusWasInside) {
    const heading = chapters[index].querySelector('h1, h2');
    heading?.setAttribute('tabindex', '-1');
    heading?.focus({ preventScroll: true });
  }
}

function showChapter(index, animate = true) {
  if (index < 0 || index >= chapters.length) return;
  if (index === activeIndex) { renderChapter(index); return; }
  clearTimeout(turnTimer);
  clearTimeout(enterTimer);
  book.classList.remove('is-turning', 'is-entering');
  if (!animate || reducedMotion.matches || narrowScreen.matches) {
    renderChapter(index);
    return;
  }
  book.classList.add('is-turning');
  turnTimer = setTimeout(() => {
    renderChapter(index);
    book.classList.remove('is-turning');
    book.classList.add('is-entering');
    enterTimer = setTimeout(() => book.classList.remove('is-entering'), 460);
  }, 220);
}

function navigateTo(index) {
  if (index < 0 || index >= chapters.length) return;
  const key = chapters[index].dataset.chapter;
  if (window.location.hash === `#${key}`) showChapter(index);
  else window.location.hash = key;
  if (narrowScreen.matches) window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
}

chapterLinks.forEach((link) => link.addEventListener('click', (event) => {
  const index = chapters.findIndex((chapter) => chapter.dataset.chapter === link.dataset.chapterLink);
  if (index < 0) return;
  event.preventDefault();
  navigateTo(index);
}));

previousButton.addEventListener('click', () => navigateTo(activeIndex - 1));
nextButton.addEventListener('click', () => navigateTo(activeIndex + 1));
window.addEventListener('hashchange', () => {
  const index = chapterIndexFromHash();
  if (index >= 0) showChapter(index);
});

document.addEventListener('keydown', (event) => {
  const target = event.target instanceof Element ? event.target : null;
  if (event.altKey || event.ctrlKey || event.metaKey || target?.closest('input, textarea, select, [contenteditable="true"]')) return;
  if (event.key === 'ArrowRight') { event.preventDefault(); navigateTo(activeIndex + 1); }
  if (event.key === 'ArrowLeft') { event.preventDefault(); navigateTo(activeIndex - 1); }
});

const year = document.querySelector('#year');
if (year) year.textContent = String(new Date().getFullYear());
renderChapter(Math.max(0, chapterIndexFromHash()));
