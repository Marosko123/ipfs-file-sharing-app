<!-- IPFSUploader.vue (Buttons Aligned Right) -->
<template>
  <div class="uploader-container">
    <h2>IPFS File Uploader & Retriever</h2>

    <div class="upload-box">
      <label class="custom-file-upload" for="file-upload">
        <input
          ref="fileInput"
          id="file-upload"
          type="file"
          @change="selectFile"
        />
        <span v-if="selectedFile">{{ selectedFile.name }}</span>
        <span v-else>📁 Choose a file to upload</span>
      </label>
      <button
        @click="uploadFile"
        :disabled="!selectedFile || loading"
        class="upload-btn"
      >
        {{ loading ? `Uploading (${progress}%)` : 'Upload' }}
      </button>
    </div>

    <progress
      v-if="loading"
      :value="progress"
      max="100"
      class="progress-bar"
    ></progress>

    <div v-if="fileHash" class="result-box">
      <p>
        <strong>Uploaded File Hash:</strong>
          {{ fileHash }}
      </p>
      <button @click="copyToClipboard" class="copy-btn">Copy Hash</button>
    </div>

    <div class="retrieve-box">
      <input
        type="text"
        v-model="retrieveHash"
        placeholder="Enter file hash to retrieve"
        :disabled="loading"
      />
      <button
        @click="retrieveFile"
        :disabled="!retrieveHash || loading"
        class="retrieve-btn"
      >
        {{ loading ? 'Downloading...' : 'Download' }}
      </button>
    </div>

    <p
      v-if="message"
      class="message"
      :class="['status-message', error ? 'error-message' : '']"
    >
      {{ message }}
    </p>

    <IPFSHistory ref="historyComponent" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import IPFSHistory from './IPFSHistory.vue';

const fileInput = ref(null);
const selectedFile = ref(null);
const fileHash = ref('');
const retrieveHash = ref('');
const message = ref('');
const error = ref(false);
const loading = ref(false);
const progress = ref(0);
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const gatewayUrl = computed(() =>
  fileHash.value
    ? `${apiBaseUrl.replace(/:\/\/[0-9]+/, '')}/ipfs/${fileHash.value}`
    : ''
);

function selectFile(event) {
  selectedFile.value = event.target.files[0] || null;
  message.value = '';
  error.value = false;
}

async function uploadFile() {
  if (!selectedFile.value) return;

  loading.value = true;
  message.value = 'Uploading file...';
  error.value = false;
  progress.value = 0;

  const formData = new FormData();
  formData.append('file', selectedFile.value);

  try {
    const response = await axios.post(
      `${apiBaseUrl}/upload`,
      formData,
      { onUploadProgress: evt => { progress.value = Math.round((evt.loaded * 100) / evt.total); } }
    );
    fileHash.value = response.data.Hash;
    copyToClipboard();
    message.value = `✅ Uploaded! Hash copied: ${fileHash.value}`;
    historyComponent.value.addHash(fileHash.value);
    selectedFile.value = null;
    fileInput.value.value = '';
  } catch (err) {
    console.error(err);
    message.value = '❌ Upload failed!';
    error.value = true;
  } finally {
    loading.value = false;
    progress.value = 0;
  }
}

async function retrieveFile() {
  if (!retrieveHash.value) return;

  loading.value = true;
  message.value = 'Downloading file...';
  error.value = false;

  try {
    const res = await axios.get(
      `${apiBaseUrl}/retrieve/${retrieveHash.value}`,
      { responseType: 'blob' }
    );
    const url = URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', retrieveHash.value);
    document.body.appendChild(link);
    link.click();
    link.remove();

    message.value = '✅ File retrieved and downloaded!';
    historyComponent.value.addHash(retrieveHash.value);
  } catch (err) {
    console.error(err);
    message.value = '❌ Retrieval failed!';
    error.value = true;
  } finally {
    loading.value = false;
  }
}

function copyToClipboard() {
  if (fileHash.value) navigator.clipboard.writeText(fileHash.value);
}

const historyComponent = ref(null);
</script>

<style scoped>
button {
  width: 100px;
  font-weight: bold;
}

strong
{
  font-weight: bold;
}

.uploader-container {
  max-width: 800px;
  margin: auto;
  padding: 1.5rem;
  background: var(--background-muted);
  border-radius: 1rem;
  color: var(--text-primary);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.upload-box,
.retrieve-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 1rem 0;
}

.custom-file-upload {
  flex: 1;
  background: var(--surface);
  padding: 0.75rem;
  border: 2px dashed var(--primary);
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.retrieve-box input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid var(--primary);
  border-radius: 0.5rem;
  background: var(--surface);
  color: var(--text-primary);
}

.upload-btn,
.retrieve-btn,
.copy-btn {
  background: var(--primary);
  color: var(--surface);
  border: none;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}
.upload-btn:disabled,
.retrieve-btn:disabled {
  background: var(--text-secondary);
  cursor: not-allowed;
}
.upload-btn:hover:not(:disabled),
.retrieve-btn:hover:not(:disabled),
.copy-btn:hover {
  background: var(--primary-dark);
}

.progress-bar {
  width: 100%;
  margin: 0.5rem 0;
  accent-color: var(--primary);
}

.result-box {
  background: var(--surface);
  padding: 1rem;
  border-left: 4px solid var(--primary);
  border-radius: 0.5rem;
  margin-top: 1rem;
  color: var(--text-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hash-link {
  color: var(--primary-dark);
  font-weight: bold;
  word-break: break-all;
}

.message {
  margin-top: 1rem;
  font-size: 1.3rem;
}

.status-message {
  margin-top: 1rem;
  color: var(--text-secondary);
}

.error-message {
  color: var(--error);
}

.status-message.error-message {
  color: var(--error);
}

.status-message:not(.error-message) {
  color: var(--text-primary);
}

</style>
