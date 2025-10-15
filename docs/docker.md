# GMTalker Docker 部署指南

本指南介绍如何使用 Docker 和 Docker Compose 部署 GMTalker 后端服务。

---

## 📋 前提条件

### 必需软件
- Docker 20.10+ 
- Docker Compose 2.0+ (可选，用于 docker-compose 部署)

### 系统要求
- **操作系统**: Linux / Windows 10+ / macOS
- **内存**: 至少 4GB RAM
- **磁盘空间**: 至少 10GB 可用空间

### 提示
- **Docker部署不支持音频输入输出，Player和ASR无法使用Local本地模式**

---

## 🚀 方式一：使用 Docker CLI 部署

### 1. 拉取镜像

```bash
docker pull huiji2333/gmtalker:latest
```

### 2. 创建配置目录

```bash
mkdir -p ./configs
```

### 3. 运行容器

#### 基础运行（无音频设备）

```bash
docker run -d \
  --name gmtalker \
  --restart unless-stopped \
  -p 5002:5002 \
  -p 7860:7860 \
  -v $(pwd)/configs:/app/configs \
  huiji2333/gmtalker:latest
```

### 4. 查看日志

```bash
docker logs -f gmtalker
```

### 5. 停止和删除容器

```bash
# 停止容器
docker stop gmtalker

# 删除容器
docker rm gmtalker
```

---

## 🐳 方式二：使用 Docker Compose 部署（推荐）

### 1. 准备 docker-compose.yml

在项目根目录创建或使用现有的 `docker-compose.yml` 文件：

```yaml
services:
  gmtalker:
    image: huiji2333/gmtalker:latest
    container_name: gmtalker
    restart: unless-stopped
    privileged: true
    volumes:
      - ./configs:/app/configs
    ports:
      - "5002:5002"
      - "7860:7860"
```

### 2. 启动服务

```bash
# 启动服务（后台运行）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看服务状态
docker-compose ps
```

### 3. 管理服务

```bash
# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 停止并删除容器及数据卷
docker-compose down -v
```

### 4. 更新服务

```bash
# 拉取最新镜像
docker-compose pull

# 重新创建并启动容器
docker-compose up -d --force-recreate
```

---

## 🔧 配置说明

### 端口映射

| 容器端口 | 主机端口 | 说明 |
|---------|---------|------|
| 5002    | 5002    | 主服务 API 端口 |
| 7860    | 7860    | WebUI 配置界面 |

### 数据卷挂载

| 容器路径 | 主机路径 | 说明 |
|---------|---------|------|
| /app/configs | ./configs | 配置文件目录 |

---

## 🔍 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker logs gmtalker

# 检查容器状态
docker inspect gmtalker
```

### 端口被占用

```bash
# Linux/macOS 检查端口占用
sudo lsof -i :5002
sudo lsof -i :7860

# Windows 检查端口占用
netstat -ano | findstr :5002
netstat -ano | findstr :7860
```

解决方法：修改 docker-compose.yml 中的端口映射

### 配置文件权限问题

```bash
# 修改配置目录权限
chmod -R 755 ./configs
```

---

## 📱 访问服务

部署成功后，可以通过以下地址访问：

- **主服务 API**: http://localhost:5002
- **WebUI 配置界面**: http://localhost:7860

### API 测试

```bash
# 测试连接
curl http://localhost:5002/v1/chat/new

# 发送聊天请求
curl -X POST http://localhost:5002/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'
```

---

## 📚 相关文档

- [WebUI 使用指南](webui.md)
- [安装指南](install.md)
- [架构说明](relate.md)

---

## 💡 常见问题

**Q: 如何进入容器进行调试？**
```bash
docker exec -it gmtalker bash
```

**Q: 如何备份配置文件？**
```bash
tar -czf configs_backup.tar.gz ./configs
```

**Q: 如何从源码构建镜像？**
```bash
docker build -t gmtalker:custom .
```

---

## 🆘 获取帮助

如遇到问题，请：
1. 查看容器日志：`docker logs gmtalker`
2. 参考 [GitHub Issues](https://github.com/feima09/GMTalker/issues)
3. 加入技术交流群（见 README）
