import React, { useState, useMemo } from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { lightTheme, darkTheme } from './theme/theme';
import MainLayout from './components/Layout/MainLayout';
import Dashboard from './pages/Dashboard';
import Visualization from './pages/Visualization';
import CodeGeneration from './pages/CodeGeneration';
import VisualizationGenerator from './pages/VisualizationGenerator';
import Templates from './pages/Templates';
import DownloadHistory from './pages/DownloadHistory';

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [activeSection, setActiveSection] = useState('dashboard');

  const theme = useMemo(() => (darkMode ? darkTheme : lightTheme), [darkMode]);

  const handleToggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleSectionChange = (section: string) => {
    setActiveSection(section);
  };

  const handleTemplateNavigation = (template: any) => {
    // 导航到代码生成页面
    setActiveSection('code-generation');
  };

  const renderContent = () => {
    switch (activeSection) {
      case 'dashboard':
        return <Dashboard />;
      case 'visualization':
        return <Visualization />;
      case 'visualization-generator':
        return <VisualizationGenerator />;
      case 'code-generation':
        return <CodeGeneration />;
      case 'download-history':
        return <DownloadHistory />;
      case 'templates':
        return <Templates onNavigateToCodeGeneration={handleTemplateNavigation} />;
      case 'settings':
        return <div>设置页面开发中...</div>;
      default:
        return <Dashboard />;
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <MainLayout
        darkMode={darkMode}
        onToggleDarkMode={handleToggleDarkMode}
        activeSection={activeSection}
        onSectionChange={handleSectionChange}
      >
        {renderContent()}
      </MainLayout>
    </ThemeProvider>
  );
}

export default App;