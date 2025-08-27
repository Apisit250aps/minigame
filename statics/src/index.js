const { createApp } = Vue

createApp({
  delimiters: ['[{', '}]'],
  data() {
    return {
      loading: true,
      error: '',
      quiz: null,
      quizIndex: 0,

      public_questions: [],
      questions: [],
      topics: [],

      settings: {
        topic: null,       // object | null
        difficulty: null,  // 1|2|3|null
      },
    }
  },

  computed: {
    filteredQuestions() {
      return this.questions.filter(q => {
        const okTopic = !this.settings.topic || q.topic?.id === this.settings.topic.id
        const okDiff  = this.settings.difficulty == null || q.difficulty === this.settings.difficulty
        return okTopic && okDiff
      })
    },
    currentTopicName() {
      return this.settings.topic?.name || 'All topics'
    }
  },

  async mounted() {
    // สลับธีมจาก localStorage ถ้ามี
    const savedTheme = localStorage.getItem('daisy-theme') || 'light'
    document.documentElement.setAttribute('data-theme', savedTheme)

    window.addEventListener('keydown', this.handleHotkeys)

    try {
      const res = await axios.get('/api/quests/')
      this.public_questions = res.data.public_questions || []
      this.questions        = res.data.questions || []
      this.topics           = res.data.topics || []

      // default filters
      this.settings.topic = this.topics[0] || null
      this.settings.difficulty = 1

      this.startQuiz()
    } catch (e) {
      this.error = 'โหลดข้อมูลไม่สำเร็จ ลองรีเฟรชอีกครั้งได้เลยนะ'
      console.error(e)
    } finally {
      this.loading = false
    }
  },

  watch: {
    // เมื่อเปลี่ยน filter ให้รีสตาร์ทลิสต์
    'settings.topic': 'startQuiz',
    'settings.difficulty': 'startQuiz',
  },

  methods: {
    setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme)
      localStorage.setItem('daisy-theme', theme)
    },
    setTopic(topic) {
      this.settings.topic = topic
    },
    setDifficulty(diff) {
      this.settings.difficulty = diff
    },
    resetFilters() {
      this.settings.topic = null
      this.settings.difficulty = null
    },

    startQuiz() {
      // เริ่มต้นที่ข้อแรกของรายการที่กรองแล้ว (หรือสุ่มก็ได้)
      if (this.filteredQuestions.length === 0) {
        this.quiz = null
        this.quizIndex = 0
        return
      }
      this.quizIndex = 0
      this.quiz = this.filteredQuestions[this.quizIndex]
    },

    nextQuestion() {
      if (this.filteredQuestions.length === 0) return
      this.quizIndex = (this.quizIndex + 1) % this.filteredQuestions.length
      this.quiz = this.filteredQuestions[this.quizIndex]
    },

    randomize() {
      if (this.filteredQuestions.length === 0) return
      this.quizIndex = Math.floor(Math.random() * this.filteredQuestions.length)
      this.quiz = this.filteredQuestions[this.quizIndex]
    },

    showAnswer() {
      const dlg = document.getElementById('ansModal')
      if (dlg?.showModal) dlg.showModal()
    },

    handleHotkeys(e) {
      // N = next, A = answer
      if (e.key.toLowerCase() === 'n') this.nextQuestion()
      if (e.key.toLowerCase() === 'a') this.showAnswer()
    },

    difficultyLabel(d) {
      if (d == null) return 'Any'
      return d === 1 ? 'Easy' : d === 2 ? 'Medium' : 'Hard'
    },
    difficultyBadgeClass(d) {
      if (d == null) return 'badge-outline'
      return d === 1 ? 'badge-success' : d === 2 ? 'badge-warning' : 'badge-error'
    },
  },

  beforeUnmount() {
    window.removeEventListener('keydown', this.handleHotkeys)
  },
}).mount('#app')
