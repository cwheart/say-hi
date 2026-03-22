<template>
  <div class="practices-page">
    <div class="page-header">
      <h1>📚 题目管理</h1>
      <button class="btn-primary" @click="$router.push('/practices/new')">+ 新建题目</button>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>文本</th>
          <th>分类</th>
          <th>难度</th>
          <th>提示</th>
          <th>音频</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in practices" :key="p.id">
          <td class="id-cell">{{ p.id }}</td>
          <td class="text-cell" :title="p.text">{{ truncateText(p.text, 20) }}</td>
          <td><span class="cat-badge">{{ p.category }}</span></td>
          <td><span class="diff-badge" :class="p.difficulty">{{ p.difficulty }}</span></td>
          <td class="hint-cell">{{ p.hint || '-' }}</td>
          <td class="audio-cell">
            <button v-if="p.audio_url" class="btn-audio" :class="{ playing: playingId === p.id }" @click="handlePlayAudio(p)" title="播放音频">🔊</button>
            <span v-else class="no-audio">-</span>
          </td>
          <td class="actions">
            <button class="btn-sm btn-edit" @click="$router.push(`/practices/${p.id}/edit`)">编辑</button>
            <button class="btn-sm btn-refresh" @click="handleRegenerate(p.id)" :disabled="regeneratingId === p.id" title="重新生成音频">{{ regeneratingId === p.id ? '⏳' : '🔄' }} 音频</button>
            <button class="btn-sm btn-danger" @click="handleDelete(p.id)" :disabled="deleting">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useApi } from '../composables/useApi'
import type { Practice } from '../types'

const { getPractices, deletePractice, regenerateAudio } = useApi()

const practices = ref<Practice[]>([])
const deleting = ref(false)
const regeneratingId = ref<string | null>(null)
const playingId = ref<string | null>(null)

let currentAudio: HTMLAudioElement | null = null

function truncateText(text: string, maxLen: number): string {
  return text.length > maxLen ? text.slice(0, maxLen) + '...' : text
}

function handlePlayAudio(p: Practice) {
  if (!p.audio_url) return
  if (playingId.value === p.id) { stopAudio(); return }
  stopAudio()
  const audioUrl = p.audio_url.startsWith('http') ? p.audio_url : p.audio_url
  currentAudio = new Audio(audioUrl)
  currentAudio.addEventListener('play', () => { playingId.value = p.id })
  currentAudio.addEventListener('ended', () => { playingId.value = null; currentAudio = null })
  currentAudio.addEventListener('error', () => { playingId.value = null; currentAudio = null; alert('音频播放失败') })
  currentAudio.play()
}

function stopAudio() {
  if (currentAudio) { currentAudio.pause(); currentAudio.currentTime = 0; currentAudio = null }
  playingId.value = null
}

async function handleRegenerate(id: string) {
  regeneratingId.value = id
  try {
    const updated = await regenerateAudio(id)
    const idx = practices.value.findIndex((p) => p.id === id)
    if (idx !== -1) practices.value[idx] = updated
  } catch (e: any) {
    alert(e?.response?.data?.detail || '音频生成失败')
  } finally {
    regeneratingId.value = null
  }
}

async function fetchPractices() {
  const res = await getPractices()
  practices.value = res.items
}

async function handleDelete(id: string) {
  if (!confirm('确定删除此题目？')) return
  deleting.value = true
  try { await deletePractice(id); await fetchPractices() } finally { deleting.value = false }
}

onMounted(fetchPractices)
onUnmounted(() => { stopAudio() })
</script>

<style scoped>
.practices-page h1 { color: #1e293b; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.btn-primary { padding: 10px 20px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }
.btn-primary:hover { background: #2563eb; }
.data-table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.data-table th { text-align: left; padding: 12px 14px; font-size: 13px; color: #64748b; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 12px 14px; font-size: 14px; color: #334155; border-bottom: 1px solid #f1f5f9; }
.id-cell { font-family: monospace; font-size: 12px; max-width: 100px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.text-cell { max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.hint-cell { max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cat-badge { font-size: 12px; padding: 2px 8px; background: #e0f2fe; color: #0369a1; border-radius: 10px; font-weight: 600; }
.diff-badge { font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 600; }
.diff-badge.beginner { background: #dcfce7; color: #16a34a; }
.diff-badge.intermediate { background: #fef3c7; color: #d97706; }
.diff-badge.advanced { background: #fee2e2; color: #dc2626; }
.audio-cell { text-align: center; }
.btn-audio { background: none; border: none; font-size: 20px; cursor: pointer; padding: 4px 8px; border-radius: 6px; transition: all 0.2s; }
.btn-audio:hover { background: #f0f9ff; }
.btn-audio.playing { animation: audio-pulse 0.8s ease-in-out infinite; background: #dbeafe; }
@keyframes audio-pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.15); opacity: 0.7; } }
.no-audio { color: #cbd5e1; }
.actions { display: flex; gap: 6px; white-space: nowrap; }
.btn-sm { padding: 4px 12px; font-size: 12px; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; }
.btn-edit { background: #e0f2fe; color: #0369a1; }
.btn-edit:hover { background: #bae6fd; }
.btn-refresh { background: #f0fdf4; color: #16a34a; }
.btn-refresh:hover { background: #dcfce7; }
.btn-danger { background: #fee2e2; color: #dc2626; }
.btn-danger:hover { background: #fecaca; }
.btn-sm:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
