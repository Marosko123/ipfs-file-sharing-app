<template>
  <div class="uploader-container">
    <h2>IPFS File Uploader & Retriever</h2>

    <!-- Upload Section -->
    <div class="upload-box">
      <label for="file-upload" class="custom-file-upload">
        <input type="file" id="file-upload" @change="selectFile" />
        <span v-if="selectedFile">{{ selectedFile.name }}</span>
        <span v-else>📁 Choose a file to upload</span>
      </label>
      <button @click="uploadFile" :disabled="!selectedFile" class="upload-btn">Upload</button>
    </div>

    <!-- Upload Status -->
    <div v-if="fileHash" class="result-box">
      <p><strong>Uploaded File Hash:</strong> <span class="hash-text">{{ fileHash }}</span></p>
      <button @click="copyToClipboard" class="copy-btn">📋 Copy Hash</button>
    </div>

    <!-- File Retrieval Section -->
    <div class="retrieve-box">
      <input type="text" v-model="retrieveHash" placeholder="Enter file hash to retrieve" />
      <button @click="retrieveFile" :disabled="!retrieveHash" class="retrieve-btn">Download</button>
    </div>

    <!-- Status Message -->
    <p v-if="message" class="status-message">{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";
import IPFSHistory from "./IPFSHistory.vue"; // Import the new component

export default {
  components: {
    IPFSHistory,
  },
  data() {
    return {
      selectedFile: null,
      fileHash: "",
      retrieveHash: "",
      message: "",
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
    };
  },
  methods: {
    selectFile(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) {
        this.message = "Please select a file!";
        return;
      }

      let formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        this.message = "Uploading file...";
        let response = await axios.post(`${this.apiBaseUrl}/upload`, formData);
        this.fileHash = response.data.Hash;
        this.message = "✅ File uploaded successfully!";
        this.$refs.historyComponent.addHash(this.fileHash); // Store hash in history
      } catch (error) {
        console.error(error);
        this.message = "❌ Upload failed!";
      }
    },
    async retrieveFile() {
      if (!this.retrieveHash) {
        this.message = "Please enter a valid file hash!";
        return;
      }

      try {
        this.message = "Downloading file...";
        let response = await axios.get(`${this.apiBaseUrl}/retrieve/${this.retrieveHash}`, {
          responseType: "blob",
        });

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", this.retrieveHash);
        document.body.appendChild(link);
        link.click();
        link.remove();

        this.message = "✅ File retrieved and downloaded!";
        this.$refs.historyComponent.addHash(this.retrieveHash); // Store hash in history
      } catch (error) {
        console.error(error);
        this.message = "❌ Retrieval failed!";
      }
    },
    copyToClipboard() {
      navigator.clipboard.writeText(this.fileHash);
      this.message = "📋 Hash copied to clipboard!";
    },
  },
};
</script>

<style scoped>
.uploader-container {
  max-width: 500px;
  margin: auto;
  text-align: center;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 1.5em;
  margin-bottom: 15px;
  color: #333;
}

.upload-box,
.retrieve-box {
  margin: 15px 0;
}

.custom-file-upload {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  padding: 12px;
  border: 2px dashed #aaa;
  cursor: pointer;
  border-radius: 8px;
  width: 100%;
}

.custom-file-upload input {
  display: none;
}

.upload-btn,
.retrieve-btn,
.copy-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 10px 15px;
  margin-top: 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s ease-in-out;
}

.upload-btn:disabled,
.retrieve-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.upload-btn:hover,
.retrieve-btn:hover,
.copy-btn:hover {
  background: #388e3c;
}

.result-box {
  background: #e3f2fd;
  padding: 10px;
  border-radius: 6px;
  margin-top: 10px;
}

.hash-text {
  font-weight: bold;
  color: #0277bd;
}

.status-message {
  font-size: 1em;
  color: #333;
  margin-top: 15px;
}
</style>
