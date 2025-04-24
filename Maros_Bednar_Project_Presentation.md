# Introduction to IPFS: A Simple File Sharing Application

**Maros Bednar**  
**FIB UPC**  
**22.03.2025**

---

## 1. Problem(s) Statement / Research Question(s)

### Centralized File Storage Limitations
- Traditional file storage relies on centralized servers.
- Bottlenecks occur, reducing scalability and performance under load.

### Security and Privacy Concerns
- Centralized systems may not ensure privacy or security, especially for sensitive data.

### Speed of Data Transfer
- Server location affects speed — distant servers result in slow data transfer.

### Problem Statement
1. What is the problem that this project is going to address?
2. Why is the problem important?
3. Who will benefit when the problem is solved?

---

## 2. Proposal

### Decentralized Storage with IPFS
- Implementation of a Python-based file-sharing app using IPFS's distributed network to remove single points of failure.

### Content Addressing
- Files identified by unique cryptographic hashes, ensuring integrity and fast retrieval.

### Peer-to-Peer Network
- Files distributed across nodes, increasing accessibility and redundancy.
- Data fetched from the nearest peer node, potentially improving speed.

---

## 3. Hypotheses

### Increased Resilience
- No central server ⇒ more robust against censorship and failures.

### Enhanced Security
- Hash-based identification and distribution lower risk of breaches.

### Improved Performance
- Parallel downloading from closer nodes can speed up access time.

**Source:** [Filebase Blog](https://filebase.com/blog/comparing-ipfs-to-traditional-file-storage-systems)

### Alternatives
- Centralized systems (Dropbox, Google Drive): Simple but vulnerable.
- Decentralized alternatives (BitTorrent, Storj): Similar ideas, but IPFS offers stronger content addressing.

---

## 4. Experiments / Use Cases

### Development
- Build a prototype Python application with a user-friendly interface for IPFS file sharing.

### Testing
- Measure file retrieval speed and reliability vs. traditional systems.

### User Feedback
- Collect usability feedback and iteratively improve the application.

**Estimated Time:** 60 hours  
**Goal:** Deep analysis + functional prototype

---

## 5. Results

### Functional Application
- Working file-sharing tool using IPFS for decentralized operations.

### Performance Metrics
- Demonstrate improved access speeds and higher resilience.

### User Satisfaction
- Positive feedback in terms of efficiency, security, and usability.

**Success Criteria:**
- Application functions correctly.
- Hypotheses confirmed by experiment data.

---

## 6. Conclusions & Future Work

### Addressing Centralization Issues
- IPFS proves to be a reliable alternative to traditional systems.

### Future Implications
- Encourages adoption of decentralized technologies.
- Contributes to a more open, secure, and resilient internet.

---

## Annex (optional)
- Technical architecture
- Performance graphs
- IPFS integration details
