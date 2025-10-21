import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Typography,
  Box,
  Chip
} from '@mui/material';
import {
  Dashboard,
  Code,
  ViewInAr,
  Download,
  Settings,
  Help,
  AutoAwesome,
  Brush,
  History
} from '@mui/icons-material';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  activeSection: string;
  onSectionChange: (section: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ open, onClose, activeSection, onSectionChange }) => {
  const menuItems = [
    { id: 'dashboard', label: '智能生成器', icon: <Dashboard />, badge: null },
    { id: 'visualization-generator', label: 'AI可视化生成器', icon: <Brush />, badge: 'NEW' },
    { id: 'visualization', label: '3D可视化', icon: <ViewInAr />, badge: null },
    { id: 'code-generation', label: '代码生成', icon: <AutoAwesome />, badge: 'AI' },
    { id: 'download-history', label: '下载历史', icon: <History />, badge: null },
    { id: 'templates', label: '模板库', icon: <Download />, badge: null },
  ];

  const secondaryItems = [
    { id: 'settings', label: '设置', icon: <Settings /> },
    { id: 'help', label: '帮助与支持', icon: <Help /> },
  ];

  const handleItemClick = (itemId: string) => {
    onSectionChange(itemId);
    onClose();
  };

  return (
    <Drawer
      variant="temporary"
      open={open}
      onClose={onClose}
      sx={{
        width: 280,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 280,
          boxSizing: 'border-box',
          backgroundColor: 'background.paper',
          borderRight: 1,
          borderColor: 'divider',
        },
      }}
    >
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
          一图胜千言
        </Typography>
        <Typography variant="body2" color="text.secondary">
          智能3D可视化平台
        </Typography>
      </Box>
      
      <Divider />
      
      <List sx={{ px: 1 }}>
        {menuItems.map((item) => (
          <ListItem key={item.id} disablePadding sx={{ mb: 0.5 }}>
            <ListItemButton
              selected={activeSection === item.id}
              onClick={() => handleItemClick(item.id)}
              sx={{
                borderRadius: 1,
                '&.Mui-selected': {
                  backgroundColor: 'primary.main',
                  color: 'primary.contrastText',
                  '& .MuiListItemIcon-root': {
                    color: 'primary.contrastText',
                  },
                },
                '&:hover': {
                  backgroundColor: activeSection === item.id ? 'primary.dark' : 'action.hover',
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: 40 }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.label} />
              {item.badge && (
                <Chip
                  label={item.badge}
                  size="small"
                  color="secondary"
                  sx={{ ml: 1, height: 20, fontSize: '0.7rem' }}
                />
              )}
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      
      <Divider sx={{ my: 2 }} />
      
      <List sx={{ px: 1 }}>
        {secondaryItems.map((item) => (
          <ListItem key={item.id} disablePadding sx={{ mb: 0.5 }}>
            <ListItemButton
              selected={activeSection === item.id}
              onClick={() => handleItemClick(item.id)}
              sx={{
                borderRadius: 1,
                '&.Mui-selected': {
                  backgroundColor: 'action.selected',
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: 40 }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;