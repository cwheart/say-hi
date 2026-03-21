<template>
  <view class="login-page">
    <view class="login-header">
      <text class="login-title">Say Hi</text>
      <text class="login-subtitle">英语发音练习</text>
    </view>

    <view class="login-form">
      <view class="form-group">
        <text class="form-label">邮箱</text>
        <input
          class="form-input"
          type="text"
          v-model="email"
          placeholder="请输入邮箱"
          placeholder-class="input-placeholder"
          @confirm="handleLogin"
        />
      </view>

      <view class="form-group">
        <text class="form-label">密码</text>
        <input
          class="form-input"
          type="password"
          v-model="password"
          placeholder="请输入密码"
          placeholder-class="input-placeholder"
          @confirm="handleLogin"
        />
      </view>

      <text v-if="errorMsg" class="error-msg">{{ errorMsg }}</text>

      <view class="btn-primary login-btn" :class="{ disabled: loading }" @tap="handleLogin">
        <text>{{ loading ? '登录中...' : '登录' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { h5Login } from '@/utils/auth'

const email = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)

async function handleLogin() {
  if (loading.value) return

  errorMsg.value = ''

  if (!email.value.trim()) {
    errorMsg.value = '请输入邮箱'
    return
  }
  if (!password.value) {
    errorMsg.value = '请输入密码'
    return
  }

  loading.value = true
  try {
    await h5Login(email.value.trim(), password.value)
    uni.switchTab({ url: '/pages/index/index' })
  } catch (e: any) {
    errorMsg.value = e?.message?.includes('401') ? '邮箱或密码错误' : (e?.message || '登录失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60rpx 50rpx;
  background-color: #f8fafc;
}

.login-header {
  text-align: center;
  margin-bottom: 80rpx;
}

.login-title {
  font-size: 56rpx;
  font-weight: 700;
  color: #1e293b;
  display: block;
}

.login-subtitle {
  font-size: 28rpx;
  color: #94a3b8;
  margin-top: 12rpx;
  display: block;
}

.login-form {
  background-color: #ffffff;
  border-radius: 24rpx;
  padding: 50rpx 40rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
}

.form-group {
  margin-bottom: 36rpx;
}

.form-label {
  font-size: 28rpx;
  color: #475569;
  margin-bottom: 12rpx;
  display: block;
}

.form-input {
  width: 100%;
  height: 88rpx;
  border: 2rpx solid #e2e8f0;
  border-radius: 12rpx;
  padding: 0 24rpx;
  font-size: 30rpx;
  color: #1e293b;
  box-sizing: border-box;
}

.input-placeholder {
  color: #cbd5e1;
}

.error-msg {
  font-size: 26rpx;
  color: #ef4444;
  margin-bottom: 24rpx;
  display: block;
}

.login-btn {
  margin-top: 20rpx;
}

.disabled {
  opacity: 0.6;
}
</style>