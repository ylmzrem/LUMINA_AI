# LUMINA AI
**Next Generation Code Trainer & Smart Adaptive Learning Assistant**

[![Language](https://img.shields.io/badge/Language-Python-blue.svg)]()
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)]()
[![AI Core](https://img.shields.io/badge/AI_Core-Gemini_API-orange.svg)]()

*(🇹🇷 Türkçe versiyon için [aşağıya kaydırın](#lumina-ai-türkçe-versiyon))*

![Lumina AI Poster](LUMINA%20AI%20-Final.png)

## 📖 Project Overview
**Lumina AI** is a next-generation intelligent study platform built for university students and developers. It combines a Retrieval-Augmented Generation (RAG) pipeline with gamified mastery tracking, allowing users to upload multi-format documents and interact through AI-powered tutoring, quizzes, and visual mind maps.

The platform operates within a single, seamless Streamlit interface powered by Google Gemini, offering features like multiple AI personas, spaced-repetition learning, real-time translation, audio podcast generation, and algorithm complexity analysis.

## 🚀 Key Features & Core Modules

* **Dynamic Personal Workspace:** Multi-format document ingestion (PDF, DOCX, TXT) with gamified mastery tracking, progress analytics, and real-time study consistency monitoring.
* **Adaptive AI Tutor & Smart Sourcing:** Customizable AI personas from simplified "ELI5" to formal "Academic" mode. Instantly trace AI-generated answers back to the exact PDF page with Click-to-Source citations.
* **Spaced Repetition Flashcards:** Leitner-based 3D flashcard engine designed for maximum long-term retention. Rate difficulty to adapt the algorithm dynamically and track session performance.
* **AI Summarization & Audio Learning:** Select specific summary depths to tailor study sessions. Converts dense academic materials into structured AI podcasts with a real-time translation pipeline for global accessibility.
* **Neural Mind Mapping:** Auto-visualizes complex document structures as interactive neural mind maps, mapping conceptual hierarchies and hidden relationships to enhance cognitive understanding.
* **Hybrid Assessment Engine:** Customize quizzes by difficulty level and question count. Receive instant analytics with detailed correct/wrong feedback to identify and bridge knowledge gaps efficiently.
* **Logic Circuit & Algorithm Validator:** Transforms natural language prompts into multi-language code implementations. Performs real-time Big-O complexity analysis and generates hardware logic schemas and system architecture documentation.

## ⚙️ RAG Architecture Flow
The underlying architecture follows a structured 6-step RAG process:
1. **Upload:** Ingest PDF/DOCX/TXT files.
2. **Chunk & Embed:** LangChain text splitter.
3. **Vector Store:** ChromaDB index.
4. **RAG Retrieval:** Semantic search over embedded chunks.
5. **Gemini LLM:** AI inference.
6. **Answer + Cite:** Page-level source generation.

## 🛠️ Technology Stack
* **Core Backend:** Python
* **UI Framework:** Streamlit
* **AI Core:** Google Gemini API (Flash / Pro)
* **RAG Pipeline:** LangChain
* **Vector Store:** ChromaDB
* **Charts & Viz:** Plotly
* **Document Parsing:** PyPDF2
* **Semantic Search:** Embeddings

## 💻 Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/LUMINA-AI.git
   cd LUMINA-AI
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Gemini API key in an `.env` file or Streamlit secrets.
4. Run the application:
   ```bash
   streamlit run app.py
   ```

---
<br>

# LUMINA AI (Türkçe Versiyon)
**Yeni Nesil Kod Eğitmeni & Akıllı Adaptif Öğrenme Asistanı**

## 📖 Proje Hakkında
**Lumina AI**, üniversite öğrencileri ve geliştiriciler için tasarlanmış yeni nesil akıllı bir çalışma platformudur. Geri Getirmeyle Zenginleştirilmiş Üretim (RAG) mimarisini oyunlaştırılmış öğrenme takibi ile birleştirerek, kullanıcıların çoklu formatlarda belgeler yüklemesine ve yapay zeka destekli özel dersler, testler ve görsel zihin haritaları aracılığıyla etkileşime girmesine olanak tanır.

Google Gemini altyapısıyla desteklenen tek bir Streamlit arayüzü üzerinden; farklı yapay zeka kişilikleri, aralıklı tekrara dayalı öğrenme, gerçek zamanlı çeviri, sesli podcast oluşturma ve algoritma karmaşıklığı analizi gibi yenilikçi özellikler sunar.

## 🚀 Temel Özellikler ve Modüller

* **Dinamik Kişisel Çalışma Alanı:** Çoklu formatta (PDF, DOCX, TXT) belge yükleme, oyunlaştırılmış ustalık takibi, ilerleme analitikleri ve gerçek zamanlı çalışma tutarlılığı izleme.
* **Adaptif Yapay Zeka Eğitmeni:** "5 Yaşındayım (ELI5)" modundan "Akademik" moda kadar özelleştirilebilir yapay zeka kişilikleri. "Kaynağa Tıkla" (Click-to-Source) özelliği sayesinde yapay zeka yanıtlarını belgedeki tam sayfasına kadar takip edebilme.
* **Aralıklı Tekrar Odaklı Bilgi Kartları (Flashcards):** Maksimum uzun vadeli kalıcılık için tasarlanmış Leitner tabanlı 3D bilgi kartı motoru. Algoritmayı dinamik olarak uyarlamak için zorluk derecesini oylama ve anlık oturum performansını izleme.
* **Yapay Zeka Özetleme ve İşitsel Öğrenme:** Oturumları kişiselleştirmek için özet derinliğini seçme. Karmaşık akademik materyalleri yapay zeka podcast'lerine dönüştürme ve evrensel erişilebilirlik için gerçek zamanlı çeviri boru hattı.
* **Nöral Zihin Haritalama:** Etkileşimli nöral zihin haritaları ile karmaşık belge yapılarını otomatik olarak görselleştirme. Bilişsel kavramayı artırmak için kavramsal hiyerarşileri ve gizli ilişkileri haritalandırma.
* **Hibrit Değerlendirme Motoru (Sınavlar):** Zorluk seviyesine ve soru sayısına göre özelleştirilebilir testler. Bilgi eksikliklerini anında tespit etmek için doğru/yanlış geri bildirimli detaylı anlık analitikler.
* **Mantık Devresi ve Algoritma Doğrulayıcı:** Doğal dili çok dilli kod uygulamalarına dönüştürme. Gerçek zamanlı Big-O karmaşıklık (complexity) analizi yapma, donanım mantık şemaları ve sistem mimarisi dokümantasyonu oluşturma.

## ⚙️ RAG Mimarisi İşleyişi
Sistem, 6 adımlı yapılandırılmış bir RAG sürecini takip eder:
1. **Upload:** PDF/DOCX/TXT dosyalarının sisteme yüklenmesi.
2. **Chunk & Embed:** LangChain ile metin parçalama (splitting).
3. **Vector Store:** ChromaDB indeksleme.
4. **RAG Retrieval:** Parçalar üzerinde anlamsal (semantic) arama.
5. **Gemini LLM:** Yapay zeka çıkarımı (inference).
6. **Answer + Cite:** Sayfa düzeyinde kaynak belirterek yanıt oluşturma.

## 🛠️ Teknoloji Yığını
* **Ana Arka Uç (Backend):** Python
* **Arayüz (UI) Çerçevesi:** Streamlit
* **Yapay Zeka Çekirdeği:** Google Gemini API (Flash / Pro)
* **RAG Mimarisi:** LangChain
* **Vektör Veritabanı:** ChromaDB
* **Grafik ve Görselleştirme:** Plotly
* **Doküman Ayrıştırma:** PyPDF2
* **Anlamsal Arama (Semantic Search):** Embeddings

## 💻 Kurulum ve Kullanım

1. Projeyi bilgisayarınıza klonlayın:
   ```bash
   git clone https://github.com/kullaniciadiniz/LUMINA-AI.git
   cd LUMINA-AI
   ```
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Gemini API anahtarınızı bir `.env` dosyasına veya Streamlit *secrets* bölümüne ekleyin.
4. Uygulamayı başlatın:
   ```bash
   streamlit run app.py
   ```
