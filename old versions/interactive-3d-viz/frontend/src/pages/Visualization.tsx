import React, { useState, useRef } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Card,
  CardContent,
  CardActions,
  Chip,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Divider
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  PlayArrow as PlayIcon,
  Download as DownloadIcon,
  Code as CodeIcon,
  Visibility as PreviewIcon,
  ViewInAr as ThreeDIcon
} from '@mui/icons-material';
import ThreeVisualization from '../components/ThreeJS/ThreeVisualization';
import DownloadDialog from '../components/DownloadDialog';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const Visualization: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [downloadDialogOpen, setDownloadDialogOpen] = useState(false);
  const [prompt, setPrompt] = useState('');
  const [vizType, setVizType] = useState('scatter_3d');
  const [dataFile, setDataFile] = useState<File | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedCode, setGeneratedCode] = useState('');
  const [previewHtml, setPreviewHtml] = useState('');
  const [error, setError] = useState('');
  const [dependencyAnalysis, setDependencyAnalysis] = useState<any>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setDataFile(file);
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('请输入可视化描述');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      // 准备请求数据
      const requestData: any = {
        prompt: prompt,
        visualization_type: vizType,
        requirements: [],
        style_preferences: {}
      };

      // 如果有文件，先上传文件
      if (dataFile) {
        const uploadFormData = new FormData();
        uploadFormData.append('file', dataFile);
        
        const uploadResponse = await fetch('http://localhost:8000/api/v1/upload/', {
          method: 'POST',
          body: uploadFormData,
        });
        
        if (uploadResponse.ok) {
          const uploadResult = await uploadResponse.json();
          requestData.data_sample = uploadResult.file_info.preview;
        }
      }

      const response = await fetch('http://localhost:8000/api/v1/code/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error('生成失败');
      }

      const result = await response.json();
      setGeneratedCode(result.code);
      setPreviewHtml(result.preview_html);
      setDependencyAnalysis(result.dependency_analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : '生成失败');
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
          dependencies: ['plotly', 'numpy', 'pandas'], // 这里应该从生成结果中获取
          filename: 'visualization',
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
      a.download = 'visualization_package.zip';
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

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        3D可视化生成器
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        使用AI生成交互式3D可视化代码
      </Typography>

      <Grid container spacing={3}>
        {/* 左侧输入区域 */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              配置参数
            </Typography>

            <Box sx={{ mb: 3 }}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="可视化描述"
                placeholder="描述你想要创建的3D可视化，例如：创建一个3D散点图显示销售数据的地理分布..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                sx={{ mb: 2 }}
              />

              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>可视化类型</InputLabel>
                <Select
                  value={vizType}
                  label="可视化类型"
                  onChange={(e) => setVizType(e.target.value)}
                >
                  <MenuItem value="scatter_3d">3D散点图</MenuItem>
                  <MenuItem value="surface_3d">3D表面图</MenuItem>
                  <MenuItem value="mesh_3d">3D网格图</MenuItem>
                  <MenuItem value="volume_3d">体积渲染</MenuItem>
                  <MenuItem value="network_3d">网络图</MenuItem>
                  <MenuItem value="molecular">分子结构</MenuItem>
                  <MenuItem value="bar_3d">3D柱状图</MenuItem>
                  <MenuItem value="line_3d">3D线图</MenuItem>
                  <MenuItem value="heatmap_3d">3D热力图</MenuItem>
                  <MenuItem value="contour_3d">3D等高线图</MenuItem>
                  <MenuItem value="point_cloud">点云图</MenuItem>
                  <MenuItem value="terrain">地形图</MenuItem>
                  <MenuItem value="financial">金融图表</MenuItem>
                  <MenuItem value="statistical">统计图表</MenuItem>
                  <MenuItem value="geographic">地理图表</MenuItem>
                  <MenuItem value="custom">自定义</MenuItem>
                </Select>
              </FormControl>

              <Box sx={{ mb: 2 }}>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                  accept=".csv,.json,.xlsx"
                  style={{ display: 'none' }}
                />
                <Button
                  variant="outlined"
                  startIcon={<UploadIcon />}
                  onClick={() => fileInputRef.current?.click()}
                  fullWidth
                >
                  {dataFile ? dataFile.name : '上传数据文件 (可选)'}
                </Button>
              </Box>

              {dataFile && (
                <Chip
                  label={`已选择: ${dataFile.name}`}
                  onDelete={() => setDataFile(null)}
                  sx={{ mb: 2 }}
                />
              )}

              <Button
                variant="contained"
                size="large"
                startIcon={isGenerating ? <CircularProgress size={20} /> : <PlayIcon />}
                onClick={handleGenerate}
                disabled={isGenerating}
                fullWidth
              >
                {isGenerating ? '生成中...' : '生成可视化'}
              </Button>
            </Box>

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
          </Paper>
        </Grid>

        {/* 右侧结果区域 */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
              <Tabs value={tabValue} onChange={handleTabChange}>
                <Tab label="3D预览" icon={<ThreeDIcon />} />
                <Tab label="AI预览" icon={<PreviewIcon />} />
                <Tab label="代码" icon={<CodeIcon />} />
              </Tabs>
            </Box>

            <TabPanel value={tabValue} index={0}>
              <ThreeVisualization 
                visualizationType={vizType}
                width={600}
                height={400}
              />
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              {previewHtml ? (
                <Box
                  sx={{
                    border: 1,
                    borderColor: 'divider',
                    borderRadius: 1,
                    height: 400,
                    overflow: 'hidden'
                  }}
                >
                  <iframe
                    srcDoc={previewHtml}
                    style={{
                      width: '100%',
                      height: '100%',
                      border: 'none'
                    }}
                    title="可视化预览"
                  />
                </Box>
              ) : (
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: 400,
                    border: 1,
                    borderColor: 'divider',
                    borderRadius: 1,
                    bgcolor: 'grey.50'
                  }}
                >
                  <Typography color="text.secondary">
                    生成可视化后将在此显示预览
                  </Typography>
                </Box>
              )}
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              {generatedCode ? (
                <Box>
                  <Box
                    component="pre"
                    sx={{
                      bgcolor: 'grey.100',
                      p: 2,
                      borderRadius: 1,
                      overflow: 'auto',
                      maxHeight: 350,
                      fontSize: '0.875rem',
                      fontFamily: 'monospace'
                    }}
                  >
                    {generatedCode}
                  </Box>
                  <Box sx={{ mt: 2 }}>
                    <Button
                      variant="contained"
                      startIcon={<DownloadIcon />}
                      onClick={handleDownloadClick}
                    >
                      下载代码包
                    </Button>
                  </Box>
                </Box>
              ) : (
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: 400,
                    border: 1,
                    borderColor: 'divider',
                    borderRadius: 1,
                    bgcolor: 'grey.50'
                  }}
                >
                  <Typography color="text.secondary">
                    生成的代码将在此显示
                  </Typography>
                </Box>
              )}
            </TabPanel>
          </Paper>
        </Grid>
      </Grid>
      
      <DownloadDialog
        open={downloadDialogOpen}
        onClose={() => setDownloadDialogOpen(false)}
        onDownload={handleDownload}
        code={generatedCode}
        dependencies={['plotly', 'numpy', 'pandas']}
        filename="visualization"
        dependencyAnalysis={dependencyAnalysis}
      />
    </Box>
  );
};

export default Visualization;