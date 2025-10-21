import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, IconButton } from '@mui/material';
import { Brightness4, Brightness7, GitHub } from '@mui/icons-material';

interface HeaderProps {
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

const Header: React.FC<HeaderProps> = ({ darkMode, onToggleDarkMode }) => {
  return (
    <AppBar position="static" elevation={0} sx={{ backgroundColor: 'background.paper', borderBottom: 1, borderColor: 'divider' }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: 'text.primary', fontWeight: 'bold' }}>
          一图胜千言
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Button 
            color="inherit" 
            sx={{ color: 'text.primary' }}
            href="#examples"
          >
            示例
          </Button>
          
          <Button 
            color="inherit" 
            sx={{ color: 'text.primary' }}
            href="#docs"
          >
            文档
          </Button>
          
          <IconButton 
            color="inherit" 
            onClick={onToggleDarkMode}
            sx={{ color: 'text.primary' }}
          >
            {darkMode ? <Brightness7 /> : <Brightness4 />}
          </IconButton>
          
          <IconButton 
            color="inherit"
            href="https://github.com/your-username/interactive-3d-viz"
            target="_blank"
            sx={{ color: 'text.primary' }}
          >
            <GitHub />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;