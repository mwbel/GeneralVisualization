import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { Box, Paper, Typography, Button, Grid, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

interface ThreeVisualizationProps {
  data?: any[];
  visualizationType?: string;
  width?: number;
  height?: number;
}

const ThreeVisualization: React.FC<ThreeVisualizationProps> = ({
  data = [],
  visualizationType = 'scatter3d',
  width = 800,
  height = 600
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene>();
  const rendererRef = useRef<THREE.WebGLRenderer>();
  const cameraRef = useRef<THREE.PerspectiveCamera>();
  const animationIdRef = useRef<number>();
  
  const [isAnimating, setIsAnimating] = useState(false);
  const [currentVizType, setCurrentVizType] = useState(visualizationType);

  useEffect(() => {
    if (!mountRef.current) return;

    // 初始化场景
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);
    sceneRef.current = scene;

    // 初始化相机
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.set(5, 5, 5);
    camera.lookAt(0, 0, 0);
    cameraRef.current = camera;

    // 初始化渲染器
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    rendererRef.current = renderer;

    // 添加到DOM
    mountRef.current.appendChild(renderer.domElement);

    // 添加光源
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    // 添加坐标轴
    const axesHelper = new THREE.AxesHelper(5);
    scene.add(axesHelper);

    // 添加网格
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    // 创建可视化内容
    createVisualization(scene, currentVizType);

    // 添加鼠标控制
    let mouseX = 0, mouseY = 0;
    let isMouseDown = false;

    const handleMouseDown = (event: MouseEvent) => {
      isMouseDown = true;
      mouseX = event.clientX;
      mouseY = event.clientY;
    };

    const handleMouseUp = () => {
      isMouseDown = false;
    };

    const handleMouseMove = (event: MouseEvent) => {
      if (!isMouseDown) return;

      const deltaX = event.clientX - mouseX;
      const deltaY = event.clientY - mouseY;

      camera.position.x = camera.position.x * Math.cos(deltaX * 0.01) - camera.position.z * Math.sin(deltaX * 0.01);
      camera.position.z = camera.position.x * Math.sin(deltaX * 0.01) + camera.position.z * Math.cos(deltaX * 0.01);
      camera.position.y += deltaY * 0.01;

      camera.lookAt(0, 0, 0);

      mouseX = event.clientX;
      mouseY = event.clientY;
    };

    renderer.domElement.addEventListener('mousedown', handleMouseDown);
    renderer.domElement.addEventListener('mouseup', handleMouseUp);
    renderer.domElement.addEventListener('mousemove', handleMouseMove);

    // 渲染循环
    const animate = () => {
      animationIdRef.current = requestAnimationFrame(animate);
      
      if (isAnimating) {
        // 旋转场景中的对象
        scene.children.forEach(child => {
          if (child.type === 'Mesh' && child.userData.animate) {
            child.rotation.y += 0.01;
          }
        });
      }

      renderer.render(scene, camera);
    };

    animate();

    // 清理函数
    return () => {
      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current);
      }
      
      renderer.domElement.removeEventListener('mousedown', handleMouseDown);
      renderer.domElement.removeEventListener('mouseup', handleMouseUp);
      renderer.domElement.removeEventListener('mousemove', handleMouseMove);

      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      
      renderer.dispose();
    };
  }, [width, height, currentVizType, isAnimating]);

  const createVisualization = (scene: THREE.Scene, vizType: string) => {
    // 清除之前的可视化对象（保留坐标轴和网格）
    const objectsToRemove = scene.children.filter(child => 
      child.type === 'Mesh' && !child.userData.isHelper
    );
    objectsToRemove.forEach(obj => scene.remove(obj));

    switch (vizType) {
      case 'scatter3d':
        createScatter3D(scene);
        break;
      case 'surface3d':
        createSurface3D(scene);
        break;
      case 'cube':
        createAnimatedCube(scene);
        break;
      case 'sphere':
        createSphere(scene);
        break;
      default:
        createScatter3D(scene);
    }
  };

  const createScatter3D = (scene: THREE.Scene) => {
    const geometry = new THREE.SphereGeometry(0.1, 16, 16);
    const colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff];

    for (let i = 0; i < 50; i++) {
      const material = new THREE.MeshLambertMaterial({ 
        color: colors[Math.floor(Math.random() * colors.length)] 
      });
      const sphere = new THREE.Mesh(geometry, material);
      
      sphere.position.set(
        (Math.random() - 0.5) * 8,
        (Math.random() - 0.5) * 8,
        (Math.random() - 0.5) * 8
      );
      
      sphere.castShadow = true;
      sphere.receiveShadow = true;
      scene.add(sphere);
    }
  };

  const createSurface3D = (scene: THREE.Scene) => {
    const geometry = new THREE.PlaneGeometry(8, 8, 32, 32);
    const material = new THREE.MeshLambertMaterial({ 
      color: 0x00ff88, 
      wireframe: false,
      side: THREE.DoubleSide 
    });

    // 创建波浪效果
    const positions = geometry.attributes.position;
    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i);
      const y = positions.getY(i);
      const z = Math.sin(x * 0.5) * Math.cos(y * 0.5) * 2;
      positions.setZ(i, z);
    }
    positions.needsUpdate = true;
    geometry.computeVertexNormals();

    const surface = new THREE.Mesh(geometry, material);
    surface.rotation.x = -Math.PI / 2;
    surface.castShadow = true;
    surface.receiveShadow = true;
    scene.add(surface);
  };

  const createAnimatedCube = (scene: THREE.Scene) => {
    const geometry = new THREE.BoxGeometry(2, 2, 2);
    const material = new THREE.MeshLambertMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    
    cube.position.set(0, 1, 0);
    cube.castShadow = true;
    cube.receiveShadow = true;
    cube.userData.animate = true;
    
    scene.add(cube);
  };

  const createSphere = (scene: THREE.Scene) => {
    const geometry = new THREE.SphereGeometry(2, 32, 32);
    const material = new THREE.MeshLambertMaterial({ color: 0xff6600 });
    const sphere = new THREE.Mesh(geometry, material);
    
    sphere.position.set(0, 2, 0);
    sphere.castShadow = true;
    sphere.receiveShadow = true;
    
    scene.add(sphere);
  };

  const handleVisualizationTypeChange = (newType: string) => {
    setCurrentVizType(newType);
  };

  const toggleAnimation = () => {
    setIsAnimating(!isAnimating);
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Three.js 3D可视化
      </Typography>
      
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth size="small">
            <InputLabel>可视化类型</InputLabel>
            <Select
              value={currentVizType}
              label="可视化类型"
              onChange={(e) => handleVisualizationTypeChange(e.target.value)}
            >
              <MenuItem value="scatter3d">3D散点图</MenuItem>
              <MenuItem value="surface3d">3D表面图</MenuItem>
              <MenuItem value="cube">动画立方体</MenuItem>
              <MenuItem value="sphere">球体</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Button
            variant={isAnimating ? "contained" : "outlined"}
            onClick={toggleAnimation}
            fullWidth
          >
            {isAnimating ? '停止动画' : '开始动画'}
          </Button>
        </Grid>
      </Grid>

      <Box
        ref={mountRef}
        sx={{
          width: width,
          height: height,
          border: '1px solid #ddd',
          borderRadius: 1,
          overflow: 'hidden',
          '& canvas': {
            display: 'block'
          }
        }}
      />
      
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        使用鼠标拖拽来旋转视角
      </Typography>
    </Paper>
  );
};

export default ThreeVisualization;