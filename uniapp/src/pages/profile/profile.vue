<template>
  <view class="profile-page container">
    <!-- User Info -->
    <view class="card user-card">
      <view class="avatar">
        <text class="avatar-text">{{ avatarLetter }}</text>
      </view>
      <view class="user-info">
        <text class="user-name">{{ displayName }}</text>
        <text class="user-role text-muted">{{ user?.role || 'user' }}</text>
      </view>
    </view>

    <!-- Stats -->
    <view class="card stats-card">
      <view class="stat-item">
        <text class="stat-value">{{ practiceCount }}</text>
        <text class="stat-label">练习次数</text>
      </view>
    </view>

    <!-- Actions -->
    <!-- #ifdef H5 -->
    <view class="actions">
      <view class="btn-logout" @tap="handleLogout">
        <text>退出登录</text>
      </view>
    </view>
    <!-- #endif -->
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getUser, type StoredUser } from '@/utils/storage'
import { logout, ensureLogin } from '@/utils/auth'
import { get } from '@/utils/request'

const user = ref<StoredUser | null>(null)
const practiceCount = ref(0)

const displayName = computed(() => {
  if (!user.value) return ''
  // #ifdef MP-WEIXIN
  return user.value.nickname || 'WeChat User'
  // #endif
  // #ifdef H5
  return user.value.email || user.value.nickname || 'User'
  // #endif
})

const avatarLetter = computed(() => {
  const name = displayName.value
  return name ? name[0].toUpperCase() : '?'
})

function handleLogout() {
  logout()
}

onShow(async () => {
  try {
    await ensureLogin()
    user.value = getUser()

    // Load practice count
    try {
      const response = await get<PaginatedResponse<any>>('/wx/history?page_size=1000')
      practiceCount.value = response.total || 0
    } catch {
      practiceCount.value = 0
    }
  } catch {
    // redirect handled by ensureLogin
  }
})
</script>

<style scoped>
.user-card {
  display: flex;
  align-items: center;
  gap: 24rpx;
  padding: 36rpx 30rpx;
}

.avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  background-color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-text {
  font-size: 40rpx;
  font-weight: 700;
  color: #ffffff;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 34rpx;
  font-weight: 600;
  color: #1e293b;
  display: block;
}

.user-role {
  font-size: 24rpx;
  display: block;
  margin-top: 6rpx;
}

.stats-card {
  display: flex;
  justify-content: center;
  padding: 36rpx;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 48rpx;
  font-weight: 700;
  color: #3b82f6;
  display: block;
}

.stat-label {
  font-size: 26rpx;
  color: #94a3b8;
  margin-top: 8rpx;
  display: block;
}

.actions {
  margin-top: 40rpx;
}

.btn-logout {
  background-color: #ffffff;
  color: #ef4444;
  border: 2rpx solid #fecaca;
  border-radius: 16rpx;
  padding: 24rpx 0;
  text-align: center;
  font-size: 30rpx;
}
</style>