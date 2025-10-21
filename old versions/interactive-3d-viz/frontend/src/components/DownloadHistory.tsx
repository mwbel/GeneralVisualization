import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  MenuItem,
  Pagination,
  Alert,
  CircularProgress,
  Tooltip,
  Stack
} from '@mui/material';
import {
  Delete,
  Download,
  Refresh,
  FilterList,
  Clear,
  TrendingUp,
  Code,
  ViewInAr
} from '@mui/icons-material';

interface DownloadRecord {
  id: string;
  filename: string;
  download_type: 'visualization' | 'code_generation';
  file_size: number;
  timestamp: string;
  dependencies?: string[];
  complexity_score?: number;
}

interface DownloadStats {
  total_downloads: number;
  total_size: number;
  most_downloaded_type: string;
  recent_downloads: number;
}

const DownloadHistory: React.FC = () => {
  const [records, setRecords] = useState<DownloadRecord[]>([]);
  const [stats, setStats] = useState<DownloadStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [filterType, setFilterType] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [recordToDelete, setRecordToDelete] = useState<string | null>(null);
  const [clearDialogOpen, setClearDialogOpen] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      // 加载下载记录
      const recordsResponse = await fetch('/api/v1/download/history');
      if (!recordsResponse.ok) {
        throw new Error('Failed to load download records');
      }
      const recordsData = await recordsResponse.json();
      setRecords(recordsData.records || []);

      // 加载统计信息
      const statsResponse = await fetch('/api/v1/download/history/stats');
      if (!statsResponse.ok) {
        throw new Error('Failed to load download stats');
      }
      const statsData = await statsResponse.json();
      setStats(statsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteRecord = async (recordId: string) => {
    try {
      const response = await fetch(`/api/v1/download/history/${recordId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete record');
      }
      await loadData();
      setDeleteDialogOpen(false);
      setRecordToDelete(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete record');
    }
  };

  const handleClearHistory = async () => {
    try {
      const response = await fetch('/api/v1/download/history', {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to clear history');
      }
      await loadData();
      setClearDialogOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to clear history');
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (timestamp: string): string => {
    return new Date(timestamp).toLocaleString('zh-CN');
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'visualization':
        return <ViewInAr color="primary" />;
      case 'code_generation':
        return <Code color="secondary" />;
      default:
        return <Download />;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'visualization':
        return '3D可视化';
      case 'code_generation':
        return '代码生成';
      default:
        return type;
    }
  };

  const filteredRecords = records.filter(record => {
    const matchesType = filterType === 'all' || record.download_type === filterType;
    const matchesSearch = record.filename.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesType && matchesSearch;
  });

  const paginatedRecords = filteredRecords.slice((page - 1) * pageSize, page * pageSize);
  const totalPages = Math.ceil(filteredRecords.length / pageSize);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        下载历史
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* 统计卡片 */}
      {stats && (
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <Download color="primary" sx={{ mr: 1 }} />
                  <Box>
                    <Typography variant="h6">{stats.total_downloads}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      总下载次数
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <TrendingUp color="success" sx={{ mr: 1 }} />
                  <Box>
                    <Typography variant="h6">{formatFileSize(stats.total_size)}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      总文件大小
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  {getTypeIcon(stats.most_downloaded_type)}
                  <Box sx={{ ml: 1 }}>
                    <Typography variant="h6">
                      {getTypeLabel(stats.most_downloaded_type)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      最常下载类型
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <Refresh color="info" sx={{ mr: 1 }} />
                  <Box>
                    <Typography variant="h6">{stats.recent_downloads}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      最近7天下载
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* 过滤和搜索 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="center">
            <TextField
              label="搜索文件名"
              variant="outlined"
              size="small"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              sx={{ minWidth: 200 }}
            />
            <TextField
              select
              label="类型筛选"
              variant="outlined"
              size="small"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              sx={{ minWidth: 150 }}
            >
              <MenuItem value="all">全部类型</MenuItem>
              <MenuItem value="visualization">3D可视化</MenuItem>
              <MenuItem value="code_generation">代码生成</MenuItem>
            </TextField>
            <Button
              variant="outlined"
              startIcon={<Refresh />}
              onClick={loadData}
            >
              刷新
            </Button>
            <Button
              variant="outlined"
              color="error"
              startIcon={<Clear />}
              onClick={() => setClearDialogOpen(true)}
              disabled={records.length === 0}
            >
              清空历史
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {/* 下载记录表格 */}
      <Card>
        <CardContent>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>文件名</TableCell>
                  <TableCell>类型</TableCell>
                  <TableCell>文件大小</TableCell>
                  <TableCell>下载时间</TableCell>
                  <TableCell>复杂度</TableCell>
                  <TableCell>依赖数量</TableCell>
                  <TableCell>操作</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {paginatedRecords.map((record) => (
                  <TableRow key={record.id}>
                    <TableCell>
                      <Typography variant="body2" fontWeight="medium">
                        {record.filename}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        icon={getTypeIcon(record.download_type)}
                        label={getTypeLabel(record.download_type)}
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>{formatFileSize(record.file_size)}</TableCell>
                    <TableCell>{formatDate(record.timestamp)}</TableCell>
                    <TableCell>
                      {record.complexity_score !== undefined ? (
                        <Chip
                          label={record.complexity_score.toFixed(1)}
                          size="small"
                          color={record.complexity_score > 7 ? 'error' : record.complexity_score > 4 ? 'warning' : 'success'}
                        />
                      ) : (
                        '-'
                      )}
                    </TableCell>
                    <TableCell>
                      {record.dependencies ? record.dependencies.length : '-'}
                    </TableCell>
                    <TableCell>
                      <Tooltip title="删除记录">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => {
                            setRecordToDelete(record.id);
                            setDeleteDialogOpen(true);
                          }}
                        >
                          <Delete />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          {filteredRecords.length === 0 && (
            <Box textAlign="center" py={4}>
              <Typography variant="body1" color="text.secondary">
                {records.length === 0 ? '暂无下载记录' : '没有符合条件的记录'}
              </Typography>
            </Box>
          )}

          {totalPages > 1 && (
            <Box display="flex" justifyContent="center" mt={2}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={(_, newPage) => setPage(newPage)}
                color="primary"
              />
            </Box>
          )}
        </CardContent>
      </Card>

      {/* 删除确认对话框 */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>确认删除</DialogTitle>
        <DialogContent>
          <Typography>确定要删除这条下载记录吗？此操作无法撤销。</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>取消</Button>
          <Button
            onClick={() => recordToDelete && handleDeleteRecord(recordToDelete)}
            color="error"
            variant="contained"
          >
            删除
          </Button>
        </DialogActions>
      </Dialog>

      {/* 清空历史确认对话框 */}
      <Dialog open={clearDialogOpen} onClose={() => setClearDialogOpen(false)}>
        <DialogTitle>确认清空历史</DialogTitle>
        <DialogContent>
          <Typography>确定要清空所有下载历史记录吗？此操作无法撤销。</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setClearDialogOpen(false)}>取消</Button>
          <Button
            onClick={handleClearHistory}
            color="error"
            variant="contained"
          >
            清空
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DownloadHistory;