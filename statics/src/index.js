const { createApp } = Vue

createApp({
  delimiters: ['[{', '}]'],
  data() {
    return {
      message: 'Hello, Vue 3!',
      public_questions: [],
      questions: [],
      topics: [],
    }
  },
  mounted() {
    this.load()
  },
  methods: {
    async load() {
      const res = await axios.get('/api/quests/')
      this.public_questions = res.data.public_questions
      this.questions = res.data.questions
      this.topics = res.data.topics
    },
  },
}).mount('#app')
