import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  AutoAwesome as AIIcon,
  Visibility as ViewIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
  Close as CloseIcon,
  Lightbulb as ExampleIcon
} from '@mui/icons-material';

interface HTMLGenerationRequest {
  prompt: string;
  visualization_type: string;
  complexity: string;
  interactivity?: boolean;
  theme?: string;
}

interface HTMLGenerationResponse {
  id: string;
  prompt: string;
  html_content: string;
  title: string;
  description: string;
  visualization_type: string;
  complexity: string;
  features: string[];
  created_at: string;
  status: string;
}

const VisualizationGenerator: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [visualizationType, setVisualizationType] = useState('custom');
  const [complexity, setComplexity] = useState('medium');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');
  const [currentVisualization, setCurrentVisualization] = useState<HTMLGenerationResponse | null>(null);
  const [previewOpen, setPreviewOpen] = useState(false);

  const examplePrompts = [
    '创建二项分布B(n,p)的交互式可视化，包含参数滑动条',
    '绘制正态分布的概率密度函数，比较不同均值和方差的影响',
    '创建3D散点图展示三个变量之间的关系',
    '可视化泊松分布的概率质量函数，展示参数λ的影响',
    '创建热力图显示相关性矩阵',
    '绘制多元线性回归的3D可视化'
  ];

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('请输入可视化需求描述');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/visualization/generate-html', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt,
          visualization_type: visualizationType,
          complexity: complexity,
          interactivity: true,
          theme: 'modern'
        } as HTMLGenerationRequest)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data: HTMLGenerationResponse = await response.json();
      setCurrentVisualization(data);
      
    } catch (err) {
      console.error('生成可视化时出错:', err);
      setError(err instanceof Error ? err.message : '生成失败，请重试');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleOpenVisualization = () => {
    if (!currentVisualization?.html_content) {
      setError('没有可用的可视化数据');
      return;
    }

    const newWindow = window.open('', '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes');
    if (newWindow) {
      newWindow.document.write(currentVisualization.html_content);
      newWindow.document.close();
    }
  };

  const handleDownloadVisualization = () => {
    if (!currentVisualization?.html_content) {
      setError('没有可用的可视化数据');
      return;
    }

    const blob = new Blob([currentVisualization.html_content], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `visualization_${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleReset = () => {
    setPrompt('');
    setCurrentVisualization(null);
    setError('');
  };

  const setExamplePrompt = (example: string) => {
    setPrompt(example);
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      {/* 页面标题 */}
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          color: 'transparent',
          fontWeight: 'bold'
        }}>
          🎨 一图胜千言
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          基于AI的交互式数据可视化创建工具
        </Typography>
        <Typography variant="body1" color="text.secondary">
          只需描述您的需求，AI将为您生成专业的交互式可视化页面
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* 左侧：输入区域 */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AIIcon color="primary" />
              描述您的可视化需求
            </Typography>
            
            <TextField
              fullWidth
              multiline
              rows={4}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="例如：创建二项分布B(n,p)的交互式可视化，包含参数滑动条..."
              variant="outlined"
              sx={{ mb: 3 }}
            />

            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>可视化类型</InputLabel>
                  <Select
                    value={visualizationType}
                    label="可视化类型"
                    onChange={(e) => setVisualizationType(e.target.value)}
                  >
                    <MenuItem value="custom">自定义</MenuItem>
                    <MenuItem value="scatter_3d">3D散点图</MenuItem>
                    <MenuItem value="surface_3d">3D表面图</MenuItem>
                    <MenuItem value="mesh_3d">3D网格图</MenuItem>
                    <MenuItem value="volume_3d">3D体积图</MenuItem>
                    <MenuItem value="bar_3d">3D柱状图</MenuItem>
                    <MenuItem value="line_3d">3D线图</MenuItem>
                    <MenuItem value="heatmap_3d">3D热力图</MenuItem>
                    <MenuItem value="point_cloud">点云图</MenuItem>
                    <MenuItem value="financial">金融图表</MenuItem>
                    <MenuItem value="statistical">统计分布图</MenuItem>
                    <MenuItem value="geographic">地理图表</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>复杂度级别</InputLabel>
                  <Select
                    value={complexity}
                    label="复杂度级别"
                    onChange={(e) => setComplexity(e.target.value)}
                  >
                    <MenuItem value="simple">简单</MenuItem>
                    <MenuItem value="medium">中等</MenuItem>
                    <MenuItem value="complex">复杂</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handleGenerate}
              disabled={isGenerating || !prompt.trim()}
              sx={{ 
                py: 2,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                }
              }}
            >
              {isGenerating ? (
                <>
                  <CircularProgress size={20} sx={{ mr: 1, color: 'white' }} />
                  AI正在生成可视化...
                </>
              ) : (
                <>
                  <AIIcon sx={{ mr: 1 }} />
                  🚀 生成可视化
                </>
              )}
            </Button>
          </Paper>

          {/* 错误提示 */}
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* 生成结果 */}
          {currentVisualization && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom color="success.main">
                ✅ 可视化生成成功！
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  <strong>{currentVisualization.title}</strong>
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {currentVisualization.description}
                </Typography>
                
                <Box sx={{ mt: 1 }}>
                  {currentVisualization.features.map((feature, index) => (
                    <Chip 
                      key={index} 
                      label={feature} 
                      size="small" 
                      sx={{ mr: 1, mb: 1 }} 
                    />
                  ))}
                </Box>
              </Box>

              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  startIcon={<ViewIcon />}
                  onClick={handleOpenVisualization}
                  color="primary"
                >
                  在新窗口中查看
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={handleDownloadVisualization}
                  color="secondary"
                >
                  下载HTML文件
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={handleReset}
                  color="info"
                >
                  生成另一个
                </Button>
              </Box>
            </Paper>
          )}
        </Grid>

        {/* 右侧：示例和帮助 */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <ExampleIcon color="primary" />
              示例提示词
            </Typography>
            
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              点击下方示例快速开始：
            </Typography>

            {examplePrompts.map((example, index) => (
              <Card 
                key={index} 
                sx={{ 
                  mb: 1, 
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  '&:hover': {
                    backgroundColor: 'action.hover',
                    transform: 'translateY(-1px)',
                    boxShadow: 2
                  }
                }}
                onClick={() => setExamplePrompt(example)}
              >
                <CardContent sx={{ py: 1.5, px: 2, '&:last-child': { pb: 1.5 } }}>
                  <Typography variant="body2">
                    • {example}
                  </Typography>
                </CardContent>
              </Card>
            ))}

            <Box sx={{ mt: 3, p: 2, backgroundColor: 'info.light', borderRadius: 1 }}>
              <Typography variant="body2" color="info.contrastText">
                💡 <strong>提示：</strong>描述越详细，生成的可视化效果越好。可以包含数据类型、交互需求、样式偏好等信息。
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default VisualizationGenerator;