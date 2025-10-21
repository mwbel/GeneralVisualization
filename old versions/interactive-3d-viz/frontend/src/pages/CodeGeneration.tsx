import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Card,
  CardContent,
  CardActions,
  Chip,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider
} from '@mui/material';
import {
  AutoAwesome as AIIcon,
  Code as CodeIcon,
  Download as DownloadIcon,
  History as HistoryIcon,
  Description as TemplateIcon
} from '@mui/icons-material';
import DownloadDialog from '../components/DownloadDialog';

interface CodeTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  complexity: string;
}

interface GenerationHistory {
  id: string;
  prompt: string;
  timestamp: string;
  success: boolean;
}

const CodeGeneration: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedCode, setGeneratedCode] = useState('');
  const [error, setError] = useState('');
  const [downloadDialogOpen, setDownloadDialogOpen] = useState(false);
  const [dependencyAnalysis, setDependencyAnalysis] = useState<any>(null);
  const [templates, setTemplates] = useState<CodeTemplate[]>([]);
  const [history, setHistory] = useState<GenerationHistory[]>([]);
  const [loadingTemplates, setLoadingTemplates] = useState(true);

  useEffect(() => {
    loadTemplates();
    loadHistory();
    
    // 检查是否有从模板页面传来的选中模板
    const selectedTemplate = localStorage.getItem('selectedTemplate');
    if (selectedTemplate) {
      try {
        const template = JSON.parse(selectedTemplate);
        // 根据模板设置初始提示
        setPrompt(`请基于${template.name}模板生成代码。${template.description}`);
        // 清除localStorage中的模板信息
        localStorage.removeItem('selectedTemplate');
      } catch (error) {
        console.error('Failed to parse selected template:', error);
      }
    }
  }, []);

  const loadTemplates = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/code/templates');
      if (response.ok) {
        const data = await response.json();
        setTemplates(data);
      }
    } catch (err) {
      console.error('Failed to load templates:', err);
    } finally {
      setLoadingTemplates(false);
    }
  };

  const loadHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/code/history');
      if (response.ok) {
        const data = await response.json();
        setHistory(data);
      }
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('请输入代码生成描述');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/code/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt,
          visualization_type: 'custom'
        }),
      });

      if (!response.ok) {
        throw new Error('代码生成失败');
      }

      const result = await response.json();
      setGeneratedCode(result.python_code);
      setDependencyAnalysis(result.dependency_analysis);
      
      // 更新历史记录
      loadHistory();
    } catch (err) {
      setError(err instanceof Error ? err.message : '代码生成失败');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = async (options: any) => {
    if (!generatedCode) {
      throw new Error('没有可下载的代码');
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/code/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: generatedCode,
          dependencies: ['numpy', 'pandas', 'matplotlib'], // 这里应该从生成结果中获取
          filename: 'generated_code',
          options: options
        }),
      });

      if (!response.ok) {
        throw new Error('下载失败');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'code_package.zip';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      throw err;
    }
  };

  const handleDownloadClick = () => {
    if (!generatedCode) {
      setError('没有可下载的代码');
      return;
    }
    setDownloadDialogOpen(true);
  };

  const handleTemplateSelect = (template: CodeTemplate) => {
    setPrompt(`基于${template.name}模板，${template.description}`);
  };

  const getComplexityColor = (complexity: string) => {
    switch (complexity.toLowerCase()) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        AI代码生成
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        使用自然语言描述生成3D可视化代码
      </Typography>

      <Grid container spacing={3}>
        {/* 左侧输入区域 */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              代码生成
            </Typography>

            <TextField
              fullWidth
              multiline
              rows={6}
              label="描述你想要的代码功能"
              placeholder="例如：创建一个交互式3D散点图，显示股票价格数据，包含缩放和旋转功能..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              sx={{ mb: 3 }}
            />

            <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
              <Button
                variant="contained"
                size="large"
                startIcon={isGenerating ? <CircularProgress size={20} /> : <AIIcon />}
                onClick={handleGenerate}
                disabled={isGenerating}
              >
                {isGenerating ? '生成中...' : '生成代码'}
              </Button>

              {generatedCode && (
                <Button
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={handleDownloadClick}
                >
                  下载代码包
                </Button>
              )}
            </Box>

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            {generatedCode && (
              <Box>
                <Typography variant="h6" gutterBottom>
                  生成的代码
                </Typography>
                <Box
                  component="pre"
                  sx={{
                    bgcolor: 'grey.100',
                    p: 2,
                    borderRadius: 1,
                    overflow: 'auto',
                    maxHeight: 400,
                    fontSize: '0.875rem',
                    fontFamily: 'monospace',
                    border: 1,
                    borderColor: 'divider'
                  }}
                >
                  {generatedCode}
                </Box>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* 右侧模板和历史 */}
        <Grid item xs={12} md={4}>
          {/* 代码模板 */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              <TemplateIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              代码模板
            </Typography>

            {loadingTemplates ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
                <CircularProgress size={24} />
              </Box>
            ) : (
              <List dense>
                {templates.map((template) => (
                  <ListItem
                    key={template.id}
                    button
                    onClick={() => handleTemplateSelect(template)}
                    sx={{ 
                      border: 1, 
                      borderColor: 'divider', 
                      borderRadius: 1, 
                      mb: 1,
                      '&:hover': {
                        bgcolor: 'action.hover'
                      }
                    }}
                  >
                    <ListItemText
                      primary={template.name}
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            {template.description}
                          </Typography>
                          <Box sx={{ mt: 1 }}>
                            <Chip 
                              label={template.category} 
                              size="small" 
                              sx={{ mr: 1 }} 
                            />
                            <Chip 
                              label={template.complexity} 
                              size="small" 
                              color={getComplexityColor(template.complexity)}
                            />
                          </Box>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>

          {/* 生成历史 */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <HistoryIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              生成历史
            </Typography>

            <List dense>
              {history.slice(0, 5).map((item) => (
                <ListItem key={item.id} sx={{ px: 0 }}>
                  <ListItemIcon>
                    <CodeIcon color={item.success ? 'success' : 'error'} />
                  </ListItemIcon>
                  <ListItemText
                    primary={item.prompt.length > 50 ? `${item.prompt.substring(0, 50)}...` : item.prompt}
                    secondary={new Date(item.timestamp).toLocaleString()}
                  />
                </ListItem>
              ))}
              {history.length === 0 && (
                <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
                  暂无生成历史
                </Typography>
              )}
            </List>
          </Paper>
        </Grid>
      </Grid>
      
      <DownloadDialog
        open={downloadDialogOpen}
        onClose={() => setDownloadDialogOpen(false)}
        onDownload={handleDownload}
        code={generatedCode}
        dependencies={['numpy', 'pandas', 'matplotlib']}
        filename="generated_code"
        dependencyAnalysis={dependencyAnalysis}
      />
    </Box>
  );
};

export default CodeGeneration;