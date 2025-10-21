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
  Alert,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import {
  Download as DownloadIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  History as HistoryIcon,
  Assessment as StatsIcon,
  Clear as ClearIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';

interface DownloadRecord {
  id: string;
  filename: string;
  code_preview: string;
  dependencies: string[];
  options: any;
  file_size: number;
  success: boolean;
  error_message?: string;
  timestamp: string;
  download_count: number;
}

interface DownloadStats {
  total_downloads: number;
  successful_downloads: number;
  failed_downloads: number;
  success_rate: number;
  most_common_dependencies: [string, number][];
  most_common_options: Record<string, number>;
  average_file_size: number;
  recent_activity: any[];
}

const DownloadHistory: React.FC = () => {
  const [records, setRecords] = useState<DownloadRecord[]>([]);
  const [stats, setStats] = useState<DownloadStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [total, setTotal] = useState(0);
  const [filterSuccess, setFilterSuccess] = useState<string>('all');
  const [selectedRecord, setSelectedRecord] = useState<DownloadRecord | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);
  const [clearDialogOpen, setClearDialogOpen] = useState(false);

  useEffect(() => {
    loadDownloadHistory();
    loadDownloadStats();
  }, [page, rowsPerPage, filterSuccess]);

  const loadDownloadHistory = async () => {
    try {
      setLoading(true);
      const filterParam = filterSuccess === 'all' ? '' : `&filter_success=${filterSuccess === 'success'}`;
      const response = await fetch(
        `http://localhost:8000/api/v1/download/history?limit=${rowsPerPage}&offset=${page * rowsPerPage}${filterParam}`
      );
      
      if (response.ok) {
        const data = await response.json();
        setRecords(data.records);
        setTotal(data.total);
      } else {
        setError('加载下载历史失败');
      }
    } catch (err) {
      setError('加载下载历史失败');
    } finally {
      setLoading(false);
    }
  };

  const loadDownloadStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/download/history/stats');
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (err) {
      console.error('加载统计信息失败:', err);
    }
  };

  const handleDeleteRecord = async (recordId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/download/history/${recordId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        loadDownloadHistory();
        loadDownloadStats();
      } else {
        setError('删除记录失败');
      }
    } catch (err) {
      setError('删除记录失败');
    }
  };

  const handleClearHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/download/history', {
        method: 'DELETE'
      });
      
      if (response.ok) {
        setClearDialogOpen(false);
        loadDownloadHistory();
        loadDownloadStats();
      } else {
        setError('清空历史失败');
      }
    } catch (err) {
      setError('清空历史失败');
    }
  };

  const handleViewDetails = (record: DownloadRecord) => {
    setSelectedRecord(record);
    setDetailDialogOpen(true);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('zh-CN');
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <HistoryIcon />
        下载历史管理
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* 统计信息卡片 */}
      {stats && (
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  总下载次数
                </Typography>
                <Typography variant="h4">
                  {stats.total_downloads}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  成功率
                </Typography>
                <Typography variant="h4" color="success.main">
                  {stats.success_rate}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  平均文件大小
                </Typography>
                <Typography variant="h4">
                  {formatFileSize(stats.average_file_size)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  失败次数
                </Typography>
                <Typography variant="h4" color="error.main">
                  {stats.failed_downloads}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* 操作栏 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>筛选状态</InputLabel>
            <Select
              value={filterSuccess}
              label="筛选状态"
              onChange={(e) => setFilterSuccess(e.target.value)}
            >
              <MenuItem value="all">全部</MenuItem>
              <MenuItem value="success">成功</MenuItem>
              <MenuItem value="failed">失败</MenuItem>
            </Select>
          </FormControl>
          <Button
            startIcon={<RefreshIcon />}
            onClick={() => {
              loadDownloadHistory();
              loadDownloadStats();
            }}
          >
            刷新
          </Button>
        </Box>
        <Button
          startIcon={<ClearIcon />}
          color="error"
          onClick={() => setClearDialogOpen(true)}
          disabled={total === 0}
        >
          清空历史
        </Button>
      </Box>

      {/* 下载记录表格 */}
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>文件名</TableCell>
                <TableCell>状态</TableCell>
                <TableCell>文件大小</TableCell>
                <TableCell>依赖数量</TableCell>
                <TableCell>下载次数</TableCell>
                <TableCell>创建时间</TableCell>
                <TableCell>操作</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : records.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    暂无下载记录
                  </TableCell>
                </TableRow>
              ) : (
                records.map((record) => (
                  <TableRow key={record.id}>
                    <TableCell>{record.filename}</TableCell>
                    <TableCell>
                      <Chip
                        label={record.success ? '成功' : '失败'}
                        color={record.success ? 'success' : 'error'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{formatFileSize(record.file_size)}</TableCell>
                    <TableCell>{record.dependencies.length}</TableCell>
                    <TableCell>{record.download_count}</TableCell>
                    <TableCell>{formatDate(record.timestamp)}</TableCell>
                    <TableCell>
                      <Tooltip title="查看详情">
                        <IconButton
                          size="small"
                          onClick={() => handleViewDetails(record)}
                        >
                          <ViewIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="删除记录">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteRecord(record.id)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          component="div"
          count={total}
          page={page}
          onPageChange={(_, newPage) => setPage(newPage)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10));
            setPage(0);
          }}
          labelRowsPerPage="每页行数:"
          labelDisplayedRows={({ from, to, count }) => `${from}-${to} 共 ${count} 条`}
        />
      </Paper>

      {/* 详情对话框 */}
      <Dialog
        open={detailDialogOpen}
        onClose={() => setDetailDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>下载记录详情</DialogTitle>
        <DialogContent>
          {selectedRecord && (
            <Box sx={{ mt: 1 }}>
              <Typography variant="h6" gutterBottom>基本信息</Typography>
              <Grid container spacing={2} sx={{ mb: 2 }}>
                <Grid item xs={6}>
                  <Typography><strong>文件名:</strong> {selectedRecord.filename}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography><strong>状态:</strong> 
                    <Chip
                      label={selectedRecord.success ? '成功' : '失败'}
                      color={selectedRecord.success ? 'success' : 'error'}
                      size="small"
                      sx={{ ml: 1 }}
                    />
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography><strong>文件大小:</strong> {formatFileSize(selectedRecord.file_size)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography><strong>下载次数:</strong> {selectedRecord.download_count}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography><strong>创建时间:</strong> {formatDate(selectedRecord.timestamp)}</Typography>
                </Grid>
              </Grid>

              <Typography variant="h6" gutterBottom>依赖包</Typography>
              <Box sx={{ mb: 2 }}>
                {selectedRecord.dependencies.map((dep, index) => (
                  <Chip key={index} label={dep} sx={{ mr: 1, mb: 1 }} />
                ))}
              </Box>

              <Typography variant="h6" gutterBottom>配置选项</Typography>
              <Box sx={{ mb: 2 }}>
                {Object.entries(selectedRecord.options).map(([key, value]) => (
                  <Typography key={key}>
                    <strong>{key}:</strong> {String(value)}
                  </Typography>
                ))}
              </Box>

              <Typography variant="h6" gutterBottom>代码预览</Typography>
              <Paper sx={{ p: 2, bgcolor: 'grey.100' }}>
                <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                  {selectedRecord.code_preview}
                </Typography>
              </Paper>

              {selectedRecord.error_message && (
                <>
                  <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>错误信息</Typography>
                  <Alert severity="error">
                    {selectedRecord.error_message}
                  </Alert>
                </>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailDialogOpen(false)}>关闭</Button>
        </DialogActions>
      </Dialog>

      {/* 清空确认对话框 */}
      <Dialog
        open={clearDialogOpen}
        onClose={() => setClearDialogOpen(false)}
      >
        <DialogTitle>确认清空历史</DialogTitle>
        <DialogContent>
          <Typography>
            确定要清空所有下载历史记录吗？此操作不可撤销。
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setClearDialogOpen(false)}>取消</Button>
          <Button onClick={handleClearHistory} color="error">
            确认清空
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DownloadHistory;