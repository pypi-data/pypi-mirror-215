import { useState } from 'react';
import { ThemeProvider, BaseStyles, Box } from '@primer/react';
import { UnderlineNav } from '@primer/react/drafts';
import { CodeIcon } from '@primer/octicons-react';
import { DatalayerGreenIcon, JupyterBaseIcon } from '@datalayer/icons-react';
import Welcome from './Welcome';
import Tester from './Tester';
import About from './About';

const Stresser = (): JSX.Element => {
  const [tab, setTab] = useState(1);
  return (
    <>
      <ThemeProvider>
        <BaseStyles>
          <Box>
            <UnderlineNav>
              <UnderlineNav.Item
                aria-current="page"
                icon={CodeIcon}
                onSelect={e => {
                  e.preventDefault();
                  setTab(1);
                }}
              >
                Welcome
              </UnderlineNav.Item>
              <UnderlineNav.Item
                icon={JupyterBaseIcon}
                onSelect={e => {
                  e.preventDefault();
                  setTab(2);
                }}
              >
                Tests
              </UnderlineNav.Item>
              <UnderlineNav.Item
                icon={DatalayerGreenIcon}
                onSelect={e => {
                  e.preventDefault();
                  setTab(3);
                }}
              >
                About
              </UnderlineNav.Item>
            </UnderlineNav>
            <Box p={3}>
              {tab === 1 && <Welcome />}
              {tab === 2 && <Tester />}
              {tab === 3 && <About />}
            </Box>
          </Box>
        </BaseStyles>
      </ThemeProvider>
    </>
  );
};

export default Stresser;
