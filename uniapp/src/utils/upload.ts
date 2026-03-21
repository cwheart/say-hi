import { getToken, clearAll } from './storage'

const BASE_URL = '/api'

interface UploadOptions {
  url: string
  filePath?: string // MP-WEIXIN: temp file path
  fileBlob?: Blob   // H5: recorded Blob
  fileName?: string
  formData?: Record<string, string>
}

interface UploadResult {
  statusCode: number
  data: any
}

export function uploadFile(options: UploadOptions): Promise<any> {
  const { url, formData = {} } = options
  const token = getToken()
  const fullUrl = `${BASE_URL}${url}`

  // #ifdef MP-WEIXIN
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: fullUrl,
      filePath: options.filePath!,
      name: 'audio',
      formData,
      header: token ? { Authorization: `Bearer ${token}` } : {},
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(res.data))
          } catch {
            resolve(res.data)
          }
        } else if (res.statusCode === 401) {
          clearAll()
          reject(new Error('Unauthorized'))
        } else {
          reject(new Error(`Upload failed: HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg || 'Upload network error'))
      },
    })
  })
  // #endif

  // #ifdef H5
  return new Promise((resolve, reject) => {
    const fd = new FormData()
    if (options.fileBlob) {
      fd.append('audio', options.fileBlob, options.fileName || 'recording.webm')
    }
    Object.entries(formData).forEach(([key, value]) => {
      fd.append(key, value)
    })

    const xhr = new XMLHttpRequest()
    xhr.open('POST', fullUrl)
    if (token) {
      xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    }

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          resolve(JSON.parse(xhr.responseText))
        } catch {
          resolve(xhr.responseText)
        }
      } else if (xhr.status === 401) {
        clearAll()
        uni.reLaunch({ url: '/pages/login/login' })
        reject(new Error('Unauthorized'))
      } else {
        reject(new Error(`Upload failed: HTTP ${xhr.status}`))
      }
    }

    xhr.onerror = () => {
      reject(new Error('Upload network error'))
    }

    xhr.send(fd)
  })
  // #endif
}