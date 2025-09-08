# Personalized Bulk Email Offer Letter System using FastAPI and Kafka

 **Automated, scalable, and modular system for sending bulk personalized offer letters asynchronously.**

## 🎯 Objective

The goal of this project is to **automate the generation and distribution of personalized offer letters** at scale. The system:

* Reads candidate details from an **Excel file**,
* Generates **customized offer letter messages**,
* Sends them via email using **Kafka-powered asynchronous pipelines**.

This architecture ensures the system is **fault-tolerant, scalable, and modular** — making it suitable for enterprise use.

---

## 🛠 Tech Stack

* **FastAPI** – REST API backend
* **Kafka (Confluent Docker Images)** – message broker
* **Kafka Producer** – sends candidate email payloads to Kafka topics
* **Kafka Consumer** – processes messages and sends actual emails
* **Docker Compose** – container orchestration
* **Pandas** – Excel file parsing
* **SMTP** – email delivery service (configured separately)

---

## ⚙️ System Components & Flow

### 1. Excel Input File

* Contains candidate details like:
  `Name | Email | Role | Offer Amount | Start Date | Location`
* Location: `send_email/app/email_list.xlsx`

### 2. FastAPI Application

* Provides `POST /send-emails` endpoint.
* Reads Excel sheet, prepares personalized message per candidate.
* Publishes each record (JSON) into Kafka via the **producer**.

### 3. Apache Kafka

* Acts as the **message broker** between FastAPI and email sender.
* Topic used: `offer_topic`
* Provides **asynchronous buffering** and **decoupled services**.

### 4. Kafka Consumer

* Background Python service.
* Continuously listens to `offer_topic`.
* Parses candidate payloads.
* Sends personalized emails using **SMTP server**.

---

## 🔑 Why Kafka?

| Feature          | Benefit                                                 |
| ---------------- | ------------------------------------------------------- |
| **Buffering**    | Prevents email overload, smoothens traffic              |
| **Asynchronous** | Non-blocking API, emails sent in background             |
| **Reliable**     | Messages persist even if mailer crashes                 |
| **Scalable**     | Multiple consumers can process in parallel              |
| **Decoupled**    | Producer (API) and Consumer (Mailer) work independently |

---

## ✅ Outcome

* Emails are **queued asynchronously** (not real-time).
* The system is **modular, fault-tolerant, and production-ready**.
* Ideal for **large-scale recruitment workflows** requiring bulk personalized offer letters.

---

## 📝 Conclusion

During this project, I gained hands-on experience with:

* **Backend Development** using FastAPI
* **Event-Driven Architecture** using Apache Kafka
* **Containerization** with Docker
* **Automated Document & Email Handling**

What started as a small learning exercise eventually became a **real-world scalable system**. The steep learning curve taught me the importance of **modularity, asynchronous design, and security best practices** in modern backend development.

This has been a highly rewarding journey, strengthening both my **technical foundation** and my **confidence as a backend engineer**.

---

## 📚 References

* [FastAPI Documentation](https://fastapi.tiangolo.com)
* [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* [Kafka Documentation](https://kafka.apache.org/documentation/)
* [Docker Documentation](https://docs.docker.com)
* [Python Documentation](https://docs.python.org/3/)

### Tutorials

* [Docker Tutorial – Apna College](https://www.youtube.com/watch?v=fqMOX6JJhGo)
* [FastAPI Full Course – Bitfumes](https://www.youtube.com/watch?v=0sOvCWFmrtA)
* [Apache Kafka in One Video (Hindi) – M Prashant](https://www.youtube.com/watch?v=9Ya44G-VX0c)

### Quick References

* GeeksforGeeks & W3Schools – syntax refreshers
* *FastAPI Guide* by Sebastián Ramírez

