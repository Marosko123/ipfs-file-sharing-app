<!-- components/ipfsUploader.vue -->
<template>
  <div class="history-container">
    <h2>📜 File Hash History</h2>

    <div v-if="hashes.length === 0" class="empty-history">
      <p>No hashes stored yet.</p>
    </div>

    <ul v-else class="hash-list">
      <li v-for="(hash, index) in hashes" :key="index" class="hash-item">
        <span class="hash-text">{{ hash }}</span>
        <button @click="copyHash(hash)" class="copy-btn">📋 Copy</button>
        <button @click="deleteHash(index)" class="delete-btn">❌</button>
      </li>
    </ul>

    <button v-if="hashes.length > 0" @click="clearHistory" class="clear-btn">🗑️ Clear All</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      hashes: [],
    };
  },
  mounted() {
    this.loadHashes();
  },
  methods: {
    loadHashes() {
      const storedHashes = localStorage.getItem("ipfsHashes");
      if (storedHashes) {
        this.hashes = JSON.parse(storedHashes);
      }
    },
    addHash(hash) {
      if (!this.hashes.includes(hash)) {
        this.hashes.unshift(hash); // Add to the top
        localStorage.setItem("ipfsHashes", JSON.stringify(this.hashes));
      }
    },
    copyHash(hash) {
      navigator.clipboard.writeText(hash);
    },
    deleteHash(index) {
      this.hashes.splice(index, 1);
      localStorage.setItem("ipfsHashes", JSON.stringify(this.hashes));
    },
    clearHistory() {
      this.hashes = [];
      localStorage.removeItem("ipfsHashes");
    },
  },
};
</script>

<style scoped>
.history-container {
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

.empty-history {
  color: #888;
}

.hash-list {
  list-style: none;
  padding: 0;
  max-height: 200px;
  overflow-y: auto;
}

.hash-item {
  background: #e3f2fd;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hash-text {
  font-weight: bold;
  color: #0277bd;
  flex-grow: 1;
  text-align: left;
}

.copy-btn,
.delete-btn,
.clear-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 6px 12px;
  margin-left: 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s ease-in-out;
}

.copy-btn:hover {
  background: #388e3c;
}

.delete-btn {
  background: #d32f2f;
}

.delete-btn:hover {
  background: #b71c1c;
}

.clear-btn {
  margin-top: 10px;
  background: #d32f2f;
  padding: 8px 15px;
}

.clear-btn:hover {
  background: #b71c1c;
}
</style>
