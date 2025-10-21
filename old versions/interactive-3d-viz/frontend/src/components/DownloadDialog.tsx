import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControl,
  FormControlLabel,
  FormGroup,
  FormLabel,
  Checkbox,
  Select,
  MenuItem,
  InputLabel,
  Box,
  Typography,
  Divider,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Download as DownloadIcon,
  Close as CloseIcon
} from '@mui/icons-material';

interface DownloadOptions {
  include_requirements: boolean;
  include_readme: boolean;
  include_sample_data: boolean;
  include_setup_script: boolean;
  include_docker: boolean;
  include_jupyter_notebook: boolean;
  python_version: string;
  package_format: string;
}

interface DownloadDialogProps {
  open: boolean;
  onClose: () => void;
  onDownload: (options: DownloadOptions) => Promise<void>;
  code: string;
  dependencies: string[];
  filename: string;
  dependencyAnalysis?: any;
}

const DownloadDialog: React.FC<DownloadDialogProps> = ({
  open,
  onClose,
  onDownload,
  code,
  dependencies,
  filename,
  dependencyAnalysis
}) => {
  const [options, setOptions] = useState<DownloadOptions>({
    include_requirements: true,
    include_readme: true,
    include_sample_data: false,
    include_setup_script: true,
    include_docker: false,
    include_jupyter_notebook: false,
    python_version: '3.8',
    package_format: 'zip'
  });

  const [isDownloading, setIsDownloading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleOptionChange = (key: keyof DownloadOptions) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setOptions(prev => ({
      ...prev,
      [key]: event.target.checked
    }));
  };

  const handleSelectChange = (key: keyof DownloadOptions) => (
    event: any
  ) => {
    setOptions(prev => ({
      ...prev,
      [key]: event.target.value
    }));
  };

  const handleDownload = async () => {
    setIsDownloading(true);
    setError('');
    
    try {
      await onDownload(options);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : '下载失败');
    } finally {
      setIsDownloading(false);
    }
  };

  const getEstimatedSize = () => {
    let size = 5; // Base size in KB
    if (options.include_requirements) size += 1;
    if (options.include_readme) size += 3;
    if (options.include_sample_data) size += 10;
    if (options.include_setup_script) size += 2;
    if (options.include_docker) size += 5;
    if (options.include_jupyter_notebook) size += 15;
    return size;
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      maxWidth="md" 
      fullWidth
      PaperProps={{
        sx: { borderRadius: 2 }
      }}
    >
      <DialogTitle sx={{ pb: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <DownloadIcon color="primary" />
          <Typography variant="h6">下载配置</Typography>
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          自定义代码包的内容和格式
        </Typography>
      </DialogTitle>

      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            包信息
          </Typography>
          <Box sx={{ bgcolor: 'grey.50', p: 2, borderRadius: 1 }}>
            <Typography variant="body2">
              <strong>文件名:</strong> {filename}
            </Typography>
            <Typography variant="body2">
              <strong>依赖数量:</strong> {dependencies.length}
            </Typography>
            <Typography variant="body2">
              <strong>预估大小:</strong> ~{getEstimatedSize()} KB
            </Typography>
            {dependencyAnalysis && (
              <>
                <Typography variant="body2">
                  <strong>代码复杂度:</strong> {dependencyAnalysis.complexity || '中等'}
                </Typography>
                <Typography variant="body2">
                  <strong>推荐Python版本:</strong> {dependencyAnalysis.python_version || '3.8+'}
                </Typography>
                {dependencyAnalysis.suggested_packages && dependencyAnalysis.suggested_packages.length > 0 && (
                  <Typography variant="body2">
                    <strong>建议额外包:</strong> {dependencyAnalysis.suggested_packages.join(', ')}
                  </Typography>
                )}
              </>
            )}
          </Box>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* 基础选项 */}
        <Box sx={{ mb: 3 }}>
          <FormLabel component="legend" sx={{ mb: 2, fontWeight: 600 }}>
            基础文件
          </FormLabel>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox
                  checked={options.include_requirements}
                  onChange={handleOptionChange('include_requirements')}
                />
              }
              label="requirements.txt - 依赖列表文件"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={options.include_readme}
                  onChange={handleOptionChange('include_readme')}
                />
              }
              label="README.md - 使用说明文档"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={options.include_setup_script}
                  onChange={handleOptionChange('include_setup_script')}
                />
              }
              label="setup.py - 安装脚本"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={options.include_sample_data}
                  onChange={handleOptionChange('include_sample_data')}
                />
              }
              label="sample_data.csv - 示例数据文件"
            />
          </FormGroup>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* 高级选项 */}
        <Box sx={{ mb: 3 }}>
          <FormLabel component="legend" sx={{ mb: 2, fontWeight: 600 }}>
            高级选项
          </FormLabel>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox
                  checked={options.include_docker}
                  onChange={handleOptionChange('include_docker')}
                />
              }
              label="Docker 配置 - Dockerfile 和 docker-compose.yml"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={options.include_jupyter_notebook}
                  onChange={handleOptionChange('include_jupyter_notebook')}
                />
              }
              label="Jupyter Notebook - 交互式笔记本版本"
            />
          </FormGroup>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* 环境配置 */}
        <Box sx={{ mb: 2 }}>
          <FormLabel component="legend" sx={{ mb: 2, fontWeight: 600 }}>
            环境配置
          </FormLabel>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Python 版本</InputLabel>
              <Select
                value={options.python_version}
                label="Python 版本"
                onChange={handleSelectChange('python_version')}
              >
                <MenuItem value="3.8">Python 3.8</MenuItem>
                <MenuItem value="3.9">Python 3.9</MenuItem>
                <MenuItem value="3.10">Python 3.10</MenuItem>
                <MenuItem value="3.11">Python 3.11</MenuItem>
              </Select>
            </FormControl>

            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>包格式</InputLabel>
              <Select
                value={options.package_format}
                label="包格式"
                onChange={handleSelectChange('package_format')}
              >
                <MenuItem value="zip">ZIP 压缩包</MenuItem>
                <MenuItem value="tar">TAR 归档</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Box>
      </DialogContent>

      <DialogActions sx={{ px: 3, pb: 3 }}>
        <Button 
          onClick={onClose} 
          disabled={isDownloading}
          startIcon={<CloseIcon />}
        >
          取消
        </Button>
        <Button
          variant="contained"
          onClick={handleDownload}
          disabled={isDownloading || !code}
          startIcon={isDownloading ? <CircularProgress size={20} /> : <DownloadIcon />}
        >
          {isDownloading ? '下载中...' : '开始下载'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DownloadDialog;