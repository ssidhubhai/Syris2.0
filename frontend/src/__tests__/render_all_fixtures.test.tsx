import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import React from 'react';
import { DigitalPaperWorkspace } from '@/components/digital_paper/DigitalPaperWorkspace';
import { DEV_FIXTURES } from '@/fixtures';

describe('Render All Fixtures Smoke Test', () => {
  for (const [key, item] of Object.entries(DEV_FIXTURES)) {
    it(`should render fixture: ${key} (${item.pattern}) without crashing`, () => {
      const { container } = render(<DigitalPaperWorkspace initialFixtureKey={key} />);
      expect(container).toBeDefined();
    });
  }
});
