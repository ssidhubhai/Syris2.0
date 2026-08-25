import '@testing-library/jest-dom';

// JSDOM patch for accessible name calculation when CSSStyleSheet rules are undefined
const originalGetComputedStyle = window.getComputedStyle.bind(window);
window.getComputedStyle = (elt: Element, pseudoElt?: string | null) => {
  try {
    return originalGetComputedStyle(elt, pseudoElt);
  } catch (e) {
    return {
      getPropertyValue: () => '',
      display: 'block',
      visibility: 'visible',
    } as unknown as CSSStyleDeclaration;
  }
};
