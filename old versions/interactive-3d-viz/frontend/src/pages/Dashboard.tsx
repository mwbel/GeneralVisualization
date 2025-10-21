import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  Container,
  Chip,
  CircularProgress,
} from '@mui/material';
import {
  AutoAwesome,
  CheckCircle,
  Download,
  Visibility,
} from '@mui/icons-material';

const Dashboard: React.FC = () => {
  const [requirement, setRequirement] = useState('');
  const [visualizationType, setVisualizationType] = useState('自定义');
  const [complexityLevel, setComplexityLevel] = useState('简单');
  const [isGenerated, setIsGenerated] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [generatedTitle, setGeneratedTitle] = useState('');
  const [error, setError] = useState('');

  // 映射中文可视化类型到英文枚举值
  const getVisualizationTypeEnum = (chineseType: string): string => {
    const typeMapping: { [key: string]: string } = {
      '3D图表': 'scatter_3d',
      '3D散点图': 'scatter_3d',
      '3D表面图': 'surface_3d',
      '3D网格图': 'mesh_3d',
      '3D体积图': 'volume_3d',
      '3D网络图': 'network_3d',
      '分子结构': 'molecular',
      '3D柱状图': 'bar_3d',
      '3D线图': 'line_3d',
      '3D热力图': 'heatmap_3d',
      '3D等高线': 'contour_3d',
      '流线图': 'streamline_3d',
      '点云图': 'point_cloud',
      '地形图': 'terrain',
      '金融图表': 'financial',
      '统计图表': 'statistical',
      '地理图表': 'geographic',
      '自定义': 'custom'
    };
    return typeMapping[chineseType] || 'custom';
  };

  const handleGenerate = async () => {
    if (!requirement.trim()) {
      setError('请输入可视化需求');
      return;
    }

    setIsGenerating(true);
    setError('');
    setIsGenerated(false);

    try {
      const response = await fetch('http://localhost:8000/api/v1/visualization/generate-html', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: requirement,
          visualization_type: getVisualizationTypeEnum(visualizationType),
          complexity: complexityLevel === '简单' ? 'simple' : complexityLevel === '中等' ? 'medium' : 'complex',
          include_interactivity: true,
          theme: 'modern'
        }),
      });

      if (!response.ok) {
        throw new Error('生成失败，请重试');
      }

      const result = await response.json();
      setGeneratedHtml(result.html_content);
      setGeneratedTitle(result.title);
      setIsGenerated(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : '生成失败，请重试');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleViewInNewWindow = () => {
    if (!generatedHtml) {
      setError('没有可查看的内容');
      return;
    }

    const newWindow = window.open('', '_blank');
    if (newWindow) {
      newWindow.document.write(generatedHtml);
      newWindow.document.close();
    } else {
      setError('无法打开新窗口，请检查浏览器设置');
    }
  };

  const handleDownloadHtml = () => {
    if (!generatedHtml) {
      setError('没有可下载的内容');
      return;
    }

    const blob = new Blob([generatedHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${generatedTitle || 'visualization'}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleGenerateAnother = () => {
    setIsGenerated(false);
    setGeneratedHtml('');
    setGeneratedTitle('');
    setError('');
    setRequirement('');
  };

  const exampleRequirements = [
    '创建一个交互式数据可视化，主要展示销售数据中的三个维度的(x,y,z)的离散数据如何不同的变化的可视化',
    '给出三维空间中的散点图，包含参数调节功能',
    '创建3D柱状图展现三个不同类别之间的关系',
    '可视化分析中的网络图显示数据，展示数据的结构',
    '创建动力学可视化系统关系'
  ];

  return (
    <Box 
      sx={{ 
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 2
      }}
    >
      <Container maxWidth="md">
        <Card 
          sx={{ 
            maxWidth: 600, 
            mx: 'auto',
            borderRadius: 3,
            boxShadow: '0 20px 40px rgba(0,0,0,0.1)'
          }}
        >
          <CardContent sx={{ p: 4 }}>
            {/* Header */}
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
                <AutoAwesome sx={{ fontSize: 32, color: '#667eea', mr: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#333' }}>
                  智能可视化生成器
                </Typography>
              </Box>
              <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
                基于AI的交互式数据可视化创建工具
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>
                输入您的可视化需求，我们将为您生成专业的交互式图表。支持统计分析、数据
                分析、科学计算等多种可视化场景。
              </Typography>
            </Box>

            {/* Input Section */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="body1" sx={{ fontWeight: 'medium', mb: 2, display: 'flex', alignItems: 'center' }}>
                📝 描述您的可视化需求
              </Typography>
              <TextField
                fullWidth
                multiline
                rows={4}
                placeholder="创建一个交互式数据可视化，主要展示销售数据中的三个维度的(x,y,z)的离散数据如何不同的变化的可视化。先确定，1d变化，然后是2d，然后是3d。"
                value={requirement}
                onChange={(e) => setRequirement(e.target.value)}
                sx={{ mb: 2 }}
              />
            </Box>

            {/* Example Suggestions */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                示例提示（点击使用）：
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {exampleRequirements.map((example, index) => (
                  <Chip
                    key={index}
                    label={example.length > 30 ? example.substring(0, 30) + '...' : example}
                    variant="outlined"
                    size="small"
                    onClick={() => setRequirement(example)}
                    sx={{ cursor: 'pointer', '&:hover': { backgroundColor: 'action.hover' } }}
                  />
                ))}
              </Box>
            </Box>

            {/* Configuration Section */}
            <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
              <FormControl fullWidth>
                <InputLabel>可视化类型</InputLabel>
                <Select
                  value={visualizationType}
                  label="可视化类型"
                  onChange={(e) => setVisualizationType(e.target.value)}
                >
                  <MenuItem value="自定义">自定义</MenuItem>
                  <MenuItem value="散点图">散点图</MenuItem>
                  <MenuItem value="柱状图">柱状图</MenuItem>
                  <MenuItem value="折线图">折线图</MenuItem>
                  <MenuItem value="3D图表">3D图表</MenuItem>
                </Select>
              </FormControl>

              <FormControl fullWidth>
                <InputLabel>复杂度级别</InputLabel>
                <Select
                  value={complexityLevel}
                  label="复杂度级别"
                  onChange={(e) => setComplexityLevel(e.target.value)}
                >
                  <MenuItem value="简单">简单</MenuItem>
                  <MenuItem value="中等">中等</MenuItem>
                  <MenuItem value="复杂">复杂</MenuItem>
                </Select>
              </FormControl>
            </Box>

            {/* Error Display */}
            {error && (
              <Alert
                severity="error"
                sx={{
                  mb: 2,
                  borderRadius: 2,
                }}
                onClose={() => setError('')}
              >
                {error}
              </Alert>
            )}

            {/* Generate Button */}
            <Button
              fullWidth
              variant="contained"
              size="large"
              startIcon={isGenerating ? <CircularProgress size={20} color="inherit" /> : <AutoAwesome />}
              onClick={handleGenerate}
              disabled={isGenerating || !requirement.trim()}
              sx={{
                py: 1.5,
                background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #5a6fd8 30%, #6a4190 90%)',
                },
                '&:disabled': {
                  background: 'linear-gradient(45deg, #ccc 30%, #999 90%)',
                  color: 'white',
                },
                mb: 3
              }}
            >
              {isGenerating ? '正在生成...' : '🎨 生成可视化'}
            </Button>

            {/* Success State */}
            {isGenerated && (
              <Alert 
                severity="success" 
                icon={<CheckCircle />}
                sx={{ mb: 2 }}
              >
                <Typography variant="body2" sx={{ fontWeight: 'medium', mb: 1 }}>
                  ✅ 可视化生成成功！
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    size="small"
                    variant="contained"
                    startIcon={<Visibility />}
                    onClick={handleViewInNewWindow}
                    sx={{ mr: 1 }}
                  >
                    在新窗口中查看
                  </Button>
                  <Button
                    size="small"
                    variant="outlined"
                    startIcon={<Download />}
                    onClick={handleDownloadHtml}
                  >
                    下载HTML文件
                  </Button>
                  <Button
                    size="small"
                    variant="outlined"
                    color="success"
                    onClick={handleGenerateAnother}
                  >
                    生成另一个
                  </Button>
                </Box>
              </Alert>
            )}
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
};

export default Dashboard;