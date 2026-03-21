<template>
  <div class="form-page">
    <h1>{{ isEdit ? '✏️ 编辑题目' : '➕ 新建题目' }}</h1>
    <form @submit.prevent="handleSubmit" class="practice-form">
      <div class="form-group">
        <label>文本 *</label>
        <input v-model="form.text" type="text" placeholder="e.g. Hello, how are you?" required />
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>分类 *</label>
          <select v-model="form.category" required>
            <option value="word">Word</option>
            <option value="phrase">Phrase</option>
            <option value="sentence">Sentence</option>
          </select>
        </div>
        <div class="form-group">
          <label>难度 *</label>
          <select v-model="form.difficulty" required>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label>提示（可选）</label>
        <input v-model="form.hint" type="text" placeholder="e.g. Focus on the 'th' sound" />
      </div>
      <div v-if="error" class="error-msg">{{ error }}</div>
      <div class="form-actions">
        <button type="button" class="btn-secondary" @click="$router.push('/practices')">取消</button>
        <button type="submit" class="btn-primary" :disabled="saving">
          {{ saving ? '保存中...' : '保存' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '../composables/useApi'
import type { PracticeForm } from '../types'

const route = useRoute()
const router = useRouter()
const { createPractice, updatePractice, getPractices } = useApi()

const isEdit = computed(() => !!route.params.id && route.params.id !== 'new')
const saving = ref(false)
const error = ref('')

const form = ref<PracticeForm>({
  text: '',
  category: 'word',
  difficulty: 'beginner',
  hint: '',
})

onMounted(async () => {
  if (isEdit.value) {
    try {
      const res = await getPractices()
      const practice = res.items.find(p => p.id === route.params.id)
      if (practice) {
        form.value = {
          text: practice.text,
          category: practice.category,
          difficulty: practice.difficulty,
          hint: practice.hint || '',
        }
      }
    } catch { /* ignore */ }
  }
})

async function handleSubmit() {
  saving.value = true
  error.value = ''
  try {
    const data = { ...form.value, hint: form.value.hint || null }
    if (isEdit.value) {
      await updatePractice(route.params.id as string, data)
    } else {
      await createPractice(data)
    }
    router.push('/practices')
  } catch (err: any) {
    error.value = err.response?.data?.detail || '保存失败'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.form-page h1 { margin-bottom: 24px; color: #1e293b; }
.practice-form { max-width: 600px; background: white; padding: 24px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 14px; font-weight: 600; color: #334155; margin-bottom: 6px; }
.form-group input, .form-group select { width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; box-sizing: border-box; }
.form-group input:focus, .form-group select:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.error-msg { color: #ef4444; font-size: 13px; margin-bottom: 12px; padding: 8px 12px; background: #fef2f2; border-radius: 6px; }
.form-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 8px; }
.btn-primary { padding: 10px 24px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }
.btn-primary:hover:not(:disabled) { background: #2563eb; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { padding: 10px 24px; background: white; color: #64748b; border: 1px solid #e2e8f0; border-radius: 8px; font-weight: 600; cursor: pointer; }
.btn-secondary:hover { background: #f8fafc; }
</style>
