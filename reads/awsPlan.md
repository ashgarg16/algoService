Got it — if we’re constraining this POC to **AWS Free Tier** only, we’ll need to tweak the earlier architecture so you don’t accidentally burn through credits or hit surprise charges.  
Here’s how I’d adapt the design:

---

## 🔄 Key Adjustments for AWS Free Tier

### 1. **Compute**
- **Original plan:** t3.small/t3.medium EC2 for app + DB.
- **Free Tier reality:**  
  - **EC2:** 750 hours/month of **t2.micro** or **t3.micro** (1 vCPU, ~1 GiB RAM) for 12 months.  
  - This is *tight* for running both app and DB on one instance, but doable for a POC with 10–15 users if you keep background jobs light.
- **Change:**  
  - Use **one t3.micro EC2** for both app and DB initially (monolith deployment).  
  - Optimize Python workers (Uvicorn with 1–2 workers, async I/O).  
  - Offload heavy backtests to **on-demand local runs** or **AWS Lambda** (Always Free: 1M requests + 400k GB-seconds/month) if possible.

---

### 2. **Database**
- **Original plan:** PostgreSQL on RDS.
- **Free Tier reality:**  
  - RDS Free Tier: 750 hours/month of **db.t3.micro** + 20 GB storage for 12 months.  
  - But running RDS + EC2 will double your free-tier hours usage — both count separately.
- **Change:**  
  - For POC: run **Postgres on the same EC2** instance to stay within one 750-hour pool.  
  - Use **Amazon S3 (Always Free: 5 GB)** for backups instead of RDS snapshots.

---

### 3. **Storage**
- **Original plan:** EBS 50–100 GB.
- **Free Tier reality:**  
  - 30 GB EBS SSD + 2 M I/O + 1 GB snapshot storage/month.
- **Change:**  
  - Keep EBS volume ≤ 30 GB.  
  - Store logs in S3 (5 GB Always Free) and rotate aggressively.

---

### 4. **Static Assets & CDN**
- **Original plan:** Serve via Nginx on EC2.
- **Free Tier reality:**  
  - CloudFront: 1 TB data out/month for 12 months (more than enough for HTML/CSS/JS).  
  - S3 static hosting: Always Free 5 GB.
- **Change:**  
  - Host static files (HTML/CSS/JS) in **S3 + CloudFront** to reduce EC2 load.

---

### 5. **Monitoring & Logs**
- **Original plan:** Prometheus + CloudWatch.
- **Free Tier reality:**  
  - CloudWatch: 10 custom metrics + 5 GB logs ingestion/month free.  
- **Change:**  
  - Use CloudWatch for basic metrics/logs; avoid high-frequency custom metrics.

---

### 6. **Secrets**
- **Original plan:** AWS Secrets Manager.
- **Free Tier reality:**  
  - Secrets Manager is **not free** beyond 30-day trial.  
- **Change:**  
  - Store secrets in **AWS Systems Manager Parameter Store** (Always Free: 10,000 parameters/month).

---

### 7. **Backtesting**
- **Original plan:** Run on EC2 worker.
- **Free Tier reality:**  
  - Heavy CPU jobs will slow down the t3.micro for all users.
- **Change:**  
  - Option A: Run backtests locally during POC.  
  - Option B: Use AWS Lambda (Always Free) for short backtests (<15 min, within memory limits).

---

## 📋 Revised Step-by-Step for Free Tier POC

1. **Provision**  
   - 1× t3.micro EC2 (Ubuntu 22.04) — app + Postgres + Nginx.
   - 30 GB EBS (gp3).
   - S3 bucket for static assets + backups.
   - CloudFront distribution for static assets.

2. **Deploy**  
   - Install Postgres locally on EC2.  
   - Deploy FastAPI + Jinja2 app via Uvicorn/Gunicorn.  
   - Nginx reverse proxy for TLS (Let’s Encrypt certbot).

3. **Configure**  
   - Parameter Store for broker API keys.  
   - CloudWatch for logs/metrics.

4. **Optimize**  
   - Aggressive log rotation to S3.  
   - Limit concurrent backtests.  
   - Use async DB queries to keep CPU low.

5. **Test & Monitor**  
   - Watch EC2 CPU/memory via CloudWatch.  
   - Keep monthly usage < 750 hours (don’t run multiple EC2s).

---

💡 **Tip:** After 12 months, Free Tier EC2/RDS hours end — plan to either:
- Migrate DB to RDS (paid) and keep EC2 small, or
- Move to Lightsail (simpler pricing) if still small-scale.

---

If you want, I can **redraw the high-level architecture diagram** showing this **Free Tier–optimized deployment** so you have a visual blueprint before you start building.  
Would you like me to prepare that next?
