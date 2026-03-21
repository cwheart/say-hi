/**
 * Cross-platform audio recorder
 * - MP-WEIXIN: uni.getRecorderManager() → mp3 file
 * - H5: MediaRecorder API → webm Blob
 */

export interface RecorderCallbacks {
  onStart?: () => void
  onStop?: (result: RecordingResult) => void
  onError?: (error: string) => void
}

export interface RecordingResult {
  /** MP-WEIXIN: temp file path; H5: empty string */
  tempFilePath: string
  /** H5: recorded Blob; MP-WEIXIN: null */
  blob: Blob | null
  /** Duration in milliseconds */
  duration: number
}

const MAX_DURATION = 30000 // 30 seconds

let isRecording = false
let startTime = 0

// #ifdef MP-WEIXIN
let recorderManager: UniApp.RecorderManager | null = null

function getMpRecorder(): UniApp.RecorderManager {
  if (!recorderManager) {
    recorderManager = uni.getRecorderManager()
  }
  return recorderManager
}
// #endif

// #ifdef H5
let mediaRecorder: MediaRecorder | null = null
let mediaStream: MediaStream | null = null
let audioChunks: Blob[] = []
let maxDurationTimer: ReturnType<typeof setTimeout> | null = null
// #endif

/**
 * Check if recording is supported on the current platform
 */
export function isRecordingSupported(): boolean {
  // #ifdef MP-WEIXIN
  return true
  // #endif

  // #ifdef H5
  return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder)
  // #endif
}

/**
 * Start recording
 */
export function startRecording(callbacks: RecorderCallbacks = {}): void {
  if (isRecording) return

  // #ifdef MP-WEIXIN
  const recorder = getMpRecorder()

  recorder.onStart(() => {
    isRecording = true
    startTime = Date.now()
    callbacks.onStart?.()
  })

  recorder.onStop((res: any) => {
    isRecording = false
    const duration = Date.now() - startTime
    callbacks.onStop?.({
      tempFilePath: res.tempFilePath,
      blob: null,
      duration,
    })
  })

  recorder.onError((err: any) => {
    isRecording = false
    callbacks.onError?.(err.errMsg || 'Recording error')
  })

  recorder.start({
    format: 'mp3',
    sampleRate: 16000,
    numberOfChannels: 1,
    encodeBitRate: 48000,
    duration: MAX_DURATION,
  } as any)
  // #endif

  // #ifdef H5
  if (!isRecordingSupported()) {
    callbacks.onError?.('请使用现代浏览器或微信小程序进行录音')
    return
  }

  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      mediaStream = stream
      audioChunks = []

      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm'

      mediaRecorder = new MediaRecorder(stream, { mimeType })

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data)
        }
      }

      mediaRecorder.onstart = () => {
        isRecording = true
        startTime = Date.now()
        callbacks.onStart?.()

        // Auto-stop after max duration
        maxDurationTimer = setTimeout(() => {
          stopRecording()
        }, MAX_DURATION)
      }

      mediaRecorder.onstop = () => {
        isRecording = false
        if (maxDurationTimer) {
          clearTimeout(maxDurationTimer)
          maxDurationTimer = null
        }

        const duration = Date.now() - startTime
        const blob = new Blob(audioChunks, { type: mimeType })
        audioChunks = []

        // Release media stream
        if (mediaStream) {
          mediaStream.getTracks().forEach((track) => track.stop())
          mediaStream = null
        }

        callbacks.onStop?.({
          tempFilePath: '',
          blob,
          duration,
        })
      }

      mediaRecorder.onerror = () => {
        isRecording = false
        if (mediaStream) {
          mediaStream.getTracks().forEach((track) => track.stop())
          mediaStream = null
        }
        callbacks.onError?.('Recording error')
      }

      mediaRecorder.start()
    })
    .catch((err) => {
      const msg =
        err.name === 'NotAllowedError'
          ? '麦克风权限被拒绝，请在浏览器设置中允许使用麦克风'
          : '无法访问麦克风'
      callbacks.onError?.(msg)
    })
  // #endif
}

/**
 * Stop recording
 */
export function stopRecording(): void {
  if (!isRecording) return

  // #ifdef MP-WEIXIN
  const recorder = getMpRecorder()
  recorder.stop()
  // #endif

  // #ifdef H5
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop()
  }
  // #endif
}

/**
 * Get current recording state
 */
export function getRecordingState(): boolean {
  return isRecording
}