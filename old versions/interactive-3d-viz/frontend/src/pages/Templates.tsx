import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tabs,
  Tab,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  Visibility as PreviewIcon,
  Code as CodeIcon,
  Download as DownloadIcon,
  Star as StarIcon,
  ExpandMore as ExpandMoreIcon,
  Category as CategoryIcon,
  Speed as DifficultyIcon,
  Label as TagIcon,
  NavigateBefore as PrevIcon,
  NavigateNext as NextIcon
} from '@mui/icons-material';

interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  difficulty: string;
  tags: string[];
  dependencies: string[];
  visualization_type: string;
  code?: string;
  explanation?: string;
  parameters?: Record<string, any>;
  examples?: Array<{
    name: string;
    description: string;
    parameters: Record<string, any>;
  }>;
}

interface TemplatesProps {
  onNavigateToCodeGeneration?: (template: Template) => void;
}

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
      id={`template-tabpanel-${index}`}
      aria-labelledby={`template-tab-${index}`}
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

const Templates: React.FC<TemplatesProps> = ({ onNavigateToCodeGeneration }) => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [templatesPerPage] = useState(12); // 每页显示12个模板

  useEffect(() => {
    loadTemplates();
    loadCategories();
  }, []);

  const loadTemplates = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/v1/code/templates');
      const data = await response.json();
      setTemplates(data.templates || []);
    } catch (error) {
      console.error('Failed to load templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await fetch('/api/v1/code/templates/categories');
      const data = await response.json();
      setCategories(data.categories || []);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const searchTemplates = async (page: number = 1) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (searchQuery) params.append('q', searchQuery);
      if (selectedCategory) params.append('category', selectedCategory);
      if (selectedDifficulty) params.append('difficulty', selectedDifficulty);
      params.append('page', page.toString());
      params.append('page_size', templatesPerPage.toString());

      const response = await fetch(`/api/v1/code/templates/search?${params}`);
      const data = await response.json();
      setTemplates(data.templates || []);
      
      // 更新分页信息
      if (data.pagination) {
        setCurrentPage(data.pagination.page);
        // 可以添加更多分页状态管理
      }
    } catch (error) {
      console.error('Failed to search templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = async (template: Template) => {
    try {
      const response = await fetch(`/api/v1/code/templates/${template.id}`);
      const data = await response.json();
      setSelectedTemplate(data.template);
      setPreviewOpen(true);
    } catch (error) {
      console.error('Failed to load template details:', error);
    }
  };

  const handleUseTemplate = (template: Template) => {
    // 将模板信息存储到localStorage
    localStorage.setItem('selectedTemplate', JSON.stringify(template));
    
    // 使用导航回调
    if (onNavigateToCodeGeneration) {
      onNavigateToCodeGeneration(template);
    } else {
      console.log('Using template:', template);
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'beginner': return 'success';
      case 'intermediate': return 'warning';
      case 'advanced': return 'error';
      default: return 'default';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'basic': return '📊';
      case 'scientific': return '🔬';
      case 'business': return '💼';
      case 'machine_learning': return '🤖';
      case 'geospatial': return '🌍';
      default: return '📈';
    }
  };

  // 重置页码当筛选条件改变时
  useEffect(() => {
    setCurrentPage(1);
    searchTemplates(1);
  }, [searchQuery, selectedCategory, selectedDifficulty]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        模板库
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        浏览和选择预设的3D可视化模板，快速开始您的项目
      </Typography>

      {/* 搜索和筛选 */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              placeholder="搜索模板..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              InputProps={{
                startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>分类</InputLabel>
              <Select
                value={selectedCategory}
                label="分类"
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                <MenuItem value="">全部分类</MenuItem>
                {categories.map((category) => (
                  <MenuItem key={category} value={category}>
                    {getCategoryIcon(category)} {category}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>难度</InputLabel>
              <Select
                value={selectedDifficulty}
                label="难度"
                onChange={(e) => setSelectedDifficulty(e.target.value)}
              >
                <MenuItem value="">全部难度</MenuItem>
                <MenuItem value="beginner">初级</MenuItem>
                <MenuItem value="intermediate">中级</MenuItem>
                <MenuItem value="advanced">高级</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="contained"
              onClick={() => searchTemplates(1)}
              startIcon={<FilterIcon />}
            >
              筛选
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* 模板列表 */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {templates.map((template: Template) => (
            <Grid item xs={12} md={6} lg={4} key={template.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                      {getCategoryIcon(template.category)} {template.name}
                    </Typography>
                    <Chip
                      label={template.difficulty}
                      size="small"
                      color={getDifficultyColor(template.difficulty)}
                    />
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {template.description}
                  </Typography>

                  <Box sx={{ mb: 2 }}>
                    <Chip
                      icon={<CategoryIcon />}
                      label={template.category}
                      size="small"
                      variant="outlined"
                      sx={{ mr: 1, mb: 1 }}
                    />
                    {template.tags.slice(0, 2).map((tag: string) => (
                      <Chip
                        key={tag}
                        icon={<TagIcon />}
                        label={tag}
                        size="small"
                        variant="outlined"
                        sx={{ mr: 1, mb: 1 }}
                      />
                    ))}
                    {template.tags.length > 2 && (
                      <Chip
                        label={`+${template.tags.length - 2}`}
                        size="small"
                        variant="outlined"
                        sx={{ mb: 1 }}
                      />
                    )}
                  </Box>

                  <Typography variant="caption" color="text.secondary">
                    依赖: {template.dependencies.join(', ')}
                  </Typography>
                </CardContent>

                <CardActions>
                  <Button
                    size="small"
                    startIcon={<PreviewIcon />}
                    onClick={() => handlePreview(template)}
                  >
                    预览
                  </Button>
                  <Button
                    size="small"
                    variant="contained"
                    startIcon={<CodeIcon />}
                    onClick={() => handleUseTemplate(template)}
                  >
                    使用模板
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* 分页控件 */}
        {templates.length > 0 && (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mt: 4 }}>
            <IconButton 
              onClick={() => searchTemplates(currentPage - 1)}
              disabled={currentPage === 1}
              sx={{ mr: 2 }}
            >
              <PrevIcon />
            </IconButton>
            
            <Typography variant="body1" sx={{ mx: 2 }}>
              第 {currentPage} 页 ({templates.length} 个模板)
            </Typography>
            
            <IconButton 
              onClick={() => searchTemplates(currentPage + 1)}
              sx={{ ml: 2 }}
            >
              <NextIcon />
            </IconButton>
          </Box>
        )}

      {templates.length === 0 && !loading && (
          <Alert severity="info" sx={{ mt: 3 }}>
            没有找到匹配的模板，请尝试调整搜索条件。
          </Alert>
        )}

      {/* 模板预览对话框 */}
      <Dialog
        open={previewOpen}
        onClose={() => setPreviewOpen(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          {selectedTemplate && (
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h6">
                {getCategoryIcon(selectedTemplate.category)} {selectedTemplate.name}
              </Typography>
              <Chip
                label={selectedTemplate.difficulty}
                color={getDifficultyColor(selectedTemplate.difficulty)}
              />
            </Box>
          )}
        </DialogTitle>
        
        <DialogContent>
          {selectedTemplate && (
            <Box>
              <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
                <Tab label="概述" />
                <Tab label="代码" />
                <Tab label="参数" />
                <Tab label="示例" />
              </Tabs>

              <TabPanel value={tabValue} index={0}>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  {selectedTemplate.description}
                </Typography>
                
                <Typography variant="h6" sx={{ mb: 1 }}>说明</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  {selectedTemplate.explanation}
                </Typography>

                <Typography variant="h6" sx={{ mb: 1 }}>标签</Typography>
                <Box sx={{ mb: 2 }}>
                  {selectedTemplate.tags.map((tag) => (
                    <Chip key={tag} label={tag} size="small" sx={{ mr: 1, mb: 1 }} />
                  ))}
                </Box>

                <Typography variant="h6" sx={{ mb: 1 }}>依赖</Typography>
                <Box>
                  {selectedTemplate.dependencies.map((dep) => (
                    <Chip key={dep} label={dep} variant="outlined" size="small" sx={{ mr: 1, mb: 1 }} />
                  ))}
                </Box>
              </TabPanel>

              <TabPanel value={tabValue} index={1}>
                <Paper sx={{ p: 2, bgcolor: 'grey.100', overflow: 'auto', maxHeight: 400 }}>
                  <Typography component="pre" sx={{ fontSize: '0.875rem', fontFamily: 'monospace' }}>
                    {selectedTemplate.code}
                  </Typography>
                </Paper>
              </TabPanel>

              <TabPanel value={tabValue} index={2}>
                {selectedTemplate.parameters && Object.keys(selectedTemplate.parameters).length > 0 ? (
                  <Box>
                    {Object.entries(selectedTemplate.parameters).map(([key, param]: [string, any]) => (
                      <Accordion key={key}>
                        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                          <Typography variant="subtitle2">{key}</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                          <Typography variant="body2" color="text.secondary">
                            类型: {param.type}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            默认值: {String(param.default)}
                          </Typography>
                          {param.min !== undefined && (
                            <Typography variant="body2" color="text.secondary">
                              最小值: {param.min}
                            </Typography>
                          )}
                          {param.max !== undefined && (
                            <Typography variant="body2" color="text.secondary">
                              最大值: {param.max}
                            </Typography>
                          )}
                          {param.options && (
                            <Typography variant="body2" color="text.secondary">
                              选项: {param.options.join(', ')}
                            </Typography>
                          )}
                        </AccordionDetails>
                      </Accordion>
                    ))}
                  </Box>
                ) : (
                  <Typography color="text.secondary">此模板没有可配置的参数</Typography>
                )}
              </TabPanel>

              <TabPanel value={tabValue} index={3}>
                {selectedTemplate.examples && selectedTemplate.examples.length > 0 ? (
                  <Box>
                    {selectedTemplate.examples.map((example, index) => (
                      <Card key={index} sx={{ mb: 2 }}>
                        <CardContent>
                          <Typography variant="h6">{example.name}</Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {example.description}
                          </Typography>
                          <Typography variant="subtitle2">参数配置:</Typography>
                          <Paper sx={{ p: 1, bgcolor: 'grey.50', mt: 1 }}>
                            <Typography component="pre" sx={{ fontSize: '0.75rem' }}>
                              {JSON.stringify(example.parameters, null, 2)}
                            </Typography>
                          </Paper>
                        </CardContent>
                      </Card>
                    ))}
                  </Box>
                ) : (
                  <Typography color="text.secondary">此模板没有示例</Typography>
                )}
              </TabPanel>
            </Box>
          )}
        </DialogContent>

        <DialogActions>
          <Button onClick={() => setPreviewOpen(false)}>
            关闭
          </Button>
          <Button
            variant="contained"
            startIcon={<CodeIcon />}
            onClick={() => {
              if (selectedTemplate) {
                handleUseTemplate(selectedTemplate);
                setPreviewOpen(false);
              }
            }}
          >
            使用此模板
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Templates;