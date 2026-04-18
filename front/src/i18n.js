const messages = {
  en: {
    questionOf: "Question {current} of {total}",
    correctCount: "{count} correct",
    nextQuestion: "Next Question",
    seeResults: "See Results",
    quizComplete: "Quiz Complete!",
    ofCorrect: "{score} of {total} correct",
    tryAgain: "Try Again",
    amazing: "Amazing! You're a true shark expert!",
    great: "Great job! You know your sharks well!",
    notBad: "Not bad! Keep learning about these fascinating creatures.",
    keepLearning: "Time to look around and learn more!"
  },
  fr: {
    questionOf: "Question {current} sur {total}",
    correctCount: "{count} correct",
    nextQuestion: "Question Suivante",
    seeResults: "Voir les Résultats",
    quizComplete: "Quiz Terminé!",
    ofCorrect: "{score} sur {total} correct",
    tryAgain: "Réessayer",
    amazing: "Incroyable! Vous êtes un véritable expert en requins!",
    great: "Bon travail! Vous connaissez bien vos requins!",
    notBad: "Pas mal! Continuez à apprendre sur ces créatures fascinantes.",
    keepLearning: "Il est temps de regarder autour et d'apprendre plus!"
  },
  es: {
    questionOf: "Pregunta {current} de {total}",
    correctCount: "{count} correctas",
    nextQuestion: "Siguiente Pregunta",
    seeResults: "Ver Resultados",
    quizComplete: "¡Quiz Completado!",
    ofCorrect: "{score} de {total} correctas",
    tryAgain: "Intentar de Nuevo",
    amazing: "¡Increíble! ¡Eres un verdadero experto en tiburones!",
    great: "¡Buen trabajo! ¡Conoces bien a tus tiburones!",
    notBad: "¡Nada mal! ¡Sigue aprendiendo sobre estas fascinantes criaturas.",
    keepLearning: "¡Es hora de mirar alrededor y aprender más!"
  }
}

const lang = (typeof window !== 'undefined' && window.DJANGO_LANGUAGE) || 'en'

export function t(key, params = {}) {
  let str = (messages[lang] && messages[lang][key]) || messages.en[key] || key
  Object.entries(params).forEach(([k, v]) => {
    str = str.replaceAll(`{${k}}`, v)
  })
  return str
}

export const locale = lang
