/**
 * Cross-platform audio player
 * - MP-WEIXIN: uni.createInnerAudioContext()
 * - H5: new Audio()
 */

export interface AudioPlayerCallbacks {
  onPlay?: () => void
  onStop?: () => void
  onError?: (error: string) => void
}

let playing = false
let callbacks: AudioPlayerCallbacks = {}

// #ifdef MP-WEIXIN
let innerAudioContext: UniApp.InnerAudioContext | null = null

function getContext(): UniApp.InnerAudioContext {
  if (!innerAudioContext) {
    innerAudioContext = uni.createInnerAudioContext()
    innerAudioContext.onPlay(() => {
      playing = true
      callbacks.onPlay?.()
    })
    innerAudioContext.onEnded(() => {
      playing = false
      callbacks.onStop?.()
    })
    innerAudioContext.onStop(() => {
      playing = false
      callbacks.onStop?.()
    })
    innerAudioContext.onError((err: any) => {
      playing = false
      callbacks.onError?.(err?.errMsg || 'Audio playback error')
    })
  }
  return innerAudioContext
}
// #endif

// #ifdef H5
let audioElement: HTMLAudioElement | null = null
// #endif

/**
 * Play audio from a URL
 */
export function playAudio(url: string, cbs: AudioPlayerCallbacks = {}): void {
  // Stop any current playback first
  stopAudio()
  callbacks = cbs

  // #ifdef MP-WEIXIN
  const ctx = getContext()
  ctx.src = url
  ctx.play()
  // #endif

  // #ifdef H5
  audioElement = new Audio(url)
  audioElement.onplay = () => {
    playing = true
    callbacks.onPlay?.()
  }
  audioElement.onended = () => {
    playing = false
    callbacks.onStop?.()
  }
  audioElement.onerror = () => {
    playing = false
    callbacks.onError?.('Audio playback error')
  }
  audioElement.play().catch((err) => {
    playing = false
    callbacks.onError?.(err?.message || 'Audio playback error')
  })
  // #endif
}

/**
 * Stop current audio playback
 */
export function stopAudio(): void {
  // #ifdef MP-WEIXIN
  if (innerAudioContext) {
    innerAudioContext.stop()
  }
  // #endif

  // #ifdef H5
  if (audioElement) {
    audioElement.pause()
    audioElement.currentTime = 0
    audioElement = null
  }
  // #endif

  playing = false
}

/**
 * Check if audio is currently playing
 */
export function isAudioPlaying(): boolean {
  return playing
}

/**
 * Clean up resources
 */
export function destroyAudioPlayer(): void {
  stopAudio()

  // #ifdef MP-WEIXIN
  if (innerAudioContext) {
    innerAudioContext.destroy()
    innerAudioContext = null
  }
  // #endif

  // #ifdef H5
  audioElement = null
  // #endif

  callbacks = {}
}