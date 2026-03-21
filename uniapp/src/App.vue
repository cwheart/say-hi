<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";

onLaunch(async () => {
  console.log("App Launch");
  // Auth check will be handled per-page or in utils/auth.ts
});

onShow(() => {
  console.log("App Show");
});

onHide(() => {
  console.log("App Hide");
});
</script>

<style>
/* Global styles */
page {
  background-color: #f8fafc;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  color: #1e293b;
  font-size: 28rpx;
  line-height: 1.6;
}

.container {
  padding: 30rpx;
}

/* Common utility classes */
.text-center {
  text-align: center;
}

.text-primary {
  color: #3b82f6;
}

.text-muted {
  color: #94a3b8;
}

.text-danger {
  color: #ef4444;
}

.text-success {
  color: #22c55e;
}

.mt-20 {
  margin-top: 20rpx;
}

.mb-20 {
  margin-bottom: 20rpx;
}

.btn-primary {
  background-color: #3b82f6;
  color: #ffffff;
  border-radius: 16rpx;
  padding: 24rpx 0;
  text-align: center;
  font-size: 32rpx;
  font-weight: 500;
}

.btn-primary:active {
  background-color: #2563eb;
}

.card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}
</style>