import { ref, onUnmounted } from 'vue'
import type { RecordingState } from '../types'

const MAX_DURATION = 30 // seconds

export function useAudioRecorder() {
  const state = ref<RecordingState>('idle')
  const audioBlob = ref<Blob | null>(null)
  const audioUrl = ref<string | null>(null)
  const duration = ref(0)
  const error = ref<string | null>(null)
  const isSupported = ref(checkBrowserSupport())

  let mediaRecorder: MediaRecorder | null = null
  let audioChunks: Blob[] = []
  let timerInterval: ReturnType<typeof setInterval> | null = null
  let audioElement: HTMLAudioElement | null = null
  let stream: MediaStream | null = null

  function checkBrowserSupport(): boolean {
    return (
      typeof navigator.mediaDevices?.getUserMedia === 'function' &&
      typeof MediaRecorder !== 'undefined'
    )
  }

  async function startRecording() {
    if (!isSupported.value) {
      error.value = 'Your browser does not support audio recording. Please use Chrome, Firefox, or Edge.'
      return
    }

    try {
      error.value = null
      audioChunks = []
      duration.value = 0

      stream = await navigator.mediaDevices.getUserMedia({ audio: true })

      mediaRecorder = new MediaRecorder(stream, {
        mimeType: getSupportedMimeType(),
      })

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data)
        }
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunks, { type: mediaRecorder?.mimeType || 'audio/webm' })
        audioBlob.value = blob

        // Revoke previous URL
        if (audioUrl.value) {
          URL.revokeObjectURL(audioUrl.value)
        }
        audioUrl.value = URL.createObjectURL(blob)
        state.value = 'recorded'
        stopTimer()
        stopStream()
      }

      mediaRecorder.start(100) // Collect data every 100ms
      state.value = 'recording'
      startTimer()
    } catch (err: any) {
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        error.value = 'Microphone permission denied. Please allow microphone access to record.'
      } else {
        error.value = `Failed to start recording: ${err.message}`
      }
      state.value = 'idle'
    }
  }

  function stopRecording() {
    if (mediaRecorder && state.value === 'recording') {
      mediaRecorder.stop()
    }
  }

  function playRecording() {
    if (!audioUrl.value) return

    audioElement = new Audio(audioUrl.value)
    audioElement.onended = () => {
      state.value = 'recorded'
    }
    audioElement.play()
    state.value = 'playing'
  }

  function stopPlaying() {
    if (audioElement) {
      audioElement.pause()
      audioElement.currentTime = 0
      audioElement = null
    }
    state.value = 'recorded'
  }

  function resetRecording() {
    stopRecording()
    stopPlaying()
    stopTimer()
    stopStream()

    if (audioUrl.value) {
      URL.revokeObjectURL(audioUrl.value)
    }

    audioBlob.value = null
    audioUrl.value = null
    duration.value = 0
    error.value = null
    state.value = 'idle'
    audioChunks = []
  }

  function startTimer() {
    timerInterval = setInterval(() => {
      duration.value++
      if (duration.value >= MAX_DURATION) {
        stopRecording()
      }
    }, 1000)
  }

  function stopTimer() {
    if (timerInterval) {
      clearInterval(timerInterval)
      timerInterval = null
    }
  }

  function stopStream() {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop())
      stream = null
    }
  }

  function getSupportedMimeType(): string {
    const types = [
      'audio/webm;codecs=opus',
      'audio/webm',
      'audio/ogg;codecs=opus',
      'audio/ogg',
    ]
    for (const type of types) {
      if (MediaRecorder.isTypeSupported(type)) {
        return type
      }
    }
    return 'audio/webm'
  }

  function formatDuration(seconds: number): string {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  onUnmounted(() => {
    resetRecording()
  })

  return {
    state,
    audioBlob,
    audioUrl,
    duration,
    error,
    isSupported,
    maxDuration: MAX_DURATION,
    startRecording,
    stopRecording,
    playRecording,
    stopPlaying,
    resetRecording,
    formatDuration,
  }
}
