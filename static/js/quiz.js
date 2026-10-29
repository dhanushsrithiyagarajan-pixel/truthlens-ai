/**
 * TruthLens AI - Scam & Misinformation Interactive Quiz (Module G)
 * 10 original educational questions covering deepfakes, phishing, fact-checking, and scam forensics.
 */

const QUIZ_QUESTIONS = [
  {
    id: 1,
    question: "You receive an urgent SMS: 'Dear Customer, your electricity will be disconnected tonight at 9:30 PM due to unpaid bill. Immediately contact Officer Sharma on 98XXXXXXXX or install Urja-Pay.apk'. What is the safest response?",
    options: [
      "Immediately call Officer Sharma to verify if the payment is really pending.",
      "Install the Urja-Pay.apk application to inspect bill history.",
      "Do not click links or install the APK; check your bill directly on your official state discom portal or utility app.",
      "Forward the SMS to family members to warn them to pay their bills."
    ],
    correctIndex: 2,
    explanation: "This is a classic utility disconnection phishing scam. Scammers induce panic with fake deadlines and push malicious APKs that steal OTPs and financial tokens. Discoms never distribute unverified APKs over SMS. Always verify directly via official discom portals or utility offices."
  },
  {
    id: 2,
    question: "A viral video appears showing a prominent minister making an inflammatory confession. The video looks slightly soft around the mouth, the eye blinks are irregular, and no mainstream news organization has reported it. What should you conclude?",
    options: [
      "It is 100% an authentic whistleblower leak that mainstream media is actively suppressing.",
      "It displays visual hallmarks of synthetic lip-sync manipulation and must be treated as unverified until independent corroboration is established.",
      "Any video on social media with high resolution must be authentic.",
      "It is definitely an AI deepfake created using Midjourney software."
    ],
    correctIndex: 1,
    explanation: "Irregular blinking, phonetic lip-sync misalignment, and absence of independent news wire coverage are strong indicators of synthetic manipulation (e.g. Wav2Lip or deepfake dubbing). Responsible verification requires withholding belief and checking established primary sources rather than asserting unproven claims."
  },
  {
    id: 3,
    question: "What does the HTTPS padlock in your browser's address bar actually signify regarding the credibility of an article?",
    options: [
      "It guarantees that the claims published on the website are fact-checked and truthful.",
      "It certifies that the website is officially approved by cybersecurity regulators.",
      "It only means the connection between your browser and the web server is encrypted; scammers can easily obtain HTTPS certificates for fraudulent sites.",
      "It indicates the website is immune to phishing and malware."
    ],
    correctIndex: 2,
    explanation: "HTTPS encrypts data in transit to prevent local eavesdropping, but it provides zero assurance regarding the honesty or accuracy of the website's content. Today, over 80% of phishing sites use free, automated SSL certificates."
  },
  {
    id: 4,
    question: "You see a dramatic photo of flood rescue workers with a caption claiming it happened yesterday in Mumbai, but the image feels familiar. Which fact-checking technique should you deploy first?",
    options: [
      "Ask the person who posted the tweet if they took the photograph personally.",
      "Perform a reverse image search (using Google Lens or TinEye) to trace the earliest publication date and original context.",
      "Wait 48 hours for someone in the comments to point out where it came from.",
      "Apply an Instagram filter to adjust brightness and look for digital watermarks."
    ],
    correctIndex: 1,
    explanation: "Recycling authentic historical photographs under false breaking news captions is one of the most common forms of misinformation. A reverse image search immediately reveals previous instances where the image was indexed, exposing false chronology."
  },
  {
    id: 5,
    question: "Which of the following offers the strongest technical protection against modern deepfake impersonations and synthetic identity fraud?",
    options: [
      "Relying solely on visual inspection to spot hand anatomy or ear asymmetry.",
      "Cryptographic provenance architectures like C2PA (Content Authenticity Initiative) that sign media at capture time.",
      "Banning all open-source machine learning models from the public internet.",
      "Converting all video files into low-resolution GIFs."
    ],
    correctIndex: 1,
    explanation: "Visual forensics degrades as generative models improve. Cryptographic provenance (like C2PA) embeds tamper-evident metadata signed by cameras and verified publishers, establishing verifiable chains of custody."
  },
  {
    id: 6,
    question: "You receive a message from an unfamiliar number offering a 'Work-from-Home Job: Earn ₹5,000/day by simply liking YouTube videos and rating hotels on Google Maps'. What type of threat is this?",
    options: [
      "A legitimate crowdsourced digital marketing employment opportunity.",
      "A task-based prepayment scam designed to pay small initial sums before demanding large 'deposit fees' to unlock higher tasks.",
      "An automated bot testing your internet connection speed.",
      "A harmless corporate survey initiative."
    ],
    correctIndex: 1,
    explanation: "Task-based scams lures victims with easy micro-payments (₹100–₹500) for trivial tasks before directing them to encrypted Telegram channels, where they are coerced into depositing large sums in fake investment schemes."
  },
  {
    id: 7,
    question: "In India, what is the official government helpline number and national portal dedicated to reporting financial cyber frauds and digital scams?",
    options: [
      "Helpline 100 / police.gov.in",
      "Helpline 1930 / National Cyber Crime Reporting Portal (cybercrime.gov.in)",
      "Helpline 108 / emergency-report.org",
      "Helpline 1091 / womenhelpline.in"
    ],
    correctIndex: 1,
    explanation: "The Ministry of Home Affairs (MHA) and Indian Cyber Crime Coordination Centre (I4C) operate National Cyber Helpline 1930 and the central portal cybercrime.gov.in for immediate reporting and halting fraudulent fund transfers."
  },
  {
    id: 8,
    question: "When evaluating a biomedical article claiming a common kitchen spice 'instantly cures all Stage 4 cancers without chemotherapy', which red flag is most critical?",
    options: [
      "The article is written in English rather than Latin.",
      "The claim lacks references to indexed clinical trials in recognized medical registries (such as CTRI, PubMed, or clinicaltrials.gov).",
      "The page has more than three images of the spice.",
      "The website domain ends in .org."
    ],
    correctIndex: 1,
    explanation: "Biomedical claims must be substantiated through rigorous, peer-reviewed clinical trials with human participant cohorts. Sweeping panacea claims for complex conditions that bypass medical consensus are hallmarks of health misinformation."
  },
  {
    id: 9,
    question: "Why can't automated AI deepfake detectors be treated as absolute, 100% reliable arbiters in legal or academic trials?",
    options: [
      "Because AI detectors suffer from false positives, compression artifact degradation, and vulnerability to adversarial perturbation.",
      "Because computers cannot process video files longer than 2 minutes.",
      "Because all deepfakes are mathematically identical to authentic camera sensors.",
      "Because law enforcement is not allowed to use technology in court."
    ],
    correctIndex: 0,
    explanation: "AI detectors are probabilistic classifiers. They can produce false alarms on low-light or heavily compressed authentic footage and fail when novel synthesis techniques emerge. Human-in-the-loop verification is indispensable."
  },
  {
    id: 10,
    question: "Before sharing an emotional breaking news post on WhatsApp or social media, what core principle should you practice?",
    options: [
      "Share it immediately with the disclaimer 'Forwarded as received, please verify'.",
      "Pause. Investigate. Verify — check primary sources and do not amplify uncorroborated claims.",
      "Only share if your close friend or relative forwarded it first.",
      "Change the font color to blue before forwarding."
    ],
    correctIndex: 1,
    explanation: "TruthLens AI's core motto 'Pause. Investigate. Verify.' reflects the cardinal rule of digital hygiene: pausing halts viral amplification, investigating checks primary sources, and verifying prevents the spread of harmful rumors."
  }
];

let currentQuestionIndex = 0;
let quizScore = 0;
let userAnswers = [];

function resetQuizState() {
  currentQuestionIndex = 0;
  quizScore = 0;
  userAnswers = [];

  document.getElementById('quiz-intro-card').style.display = 'block';
  document.getElementById('quiz-active-card').style.display = 'none';
  document.getElementById('quiz-results-card').style.display = 'none';
}

function startQuiz() {
  document.getElementById('quiz-intro-card').style.display = 'none';
  document.getElementById('quiz-active-card').style.display = 'block';
  document.getElementById('quiz-results-card').style.display = 'none';
  loadQuestion(0);
}

function loadQuestion(index) {
  currentQuestionIndex = index;
  const q = QUIZ_QUESTIONS[index];

  // Progress Bar
  const pct = Math.round(((index) / QUIZ_QUESTIONS.length) * 100);
  document.getElementById('quiz-progress-fill').style.width = `${pct}%`;
  document.getElementById('quiz-counter-text').textContent = `Question ${index + 1} of ${QUIZ_QUESTIONS.length}`;

  // Question Title
  document.getElementById('quiz-question-text').textContent = q.question;

  // Options
  const container = document.getElementById('quiz-options-container');
  container.innerHTML = q.options.map((opt, optIdx) => `
    <div class="quiz-option" id="quiz-opt-${optIdx}" onclick="selectQuizAnswer(${optIdx})">
      <span><strong>${String.fromCharCode(65 + optIdx)}.</strong> ${window.escapeHtml(opt)}</span>
      <span class="quiz-check-marker" id="opt-marker-${optIdx}"></span>
    </div>
  `).join('');

  // Hide explanation and next button
  document.getElementById('quiz-explanation-box').style.display = 'none';
  document.getElementById('quiz-next-btn').style.display = 'none';
}

function selectQuizAnswer(optIdx) {
  const q = QUIZ_QUESTIONS[currentQuestionIndex];
  const isCorrect = (optIdx === q.correctIndex);

  // Disable further clicks on options
  document.querySelectorAll('.quiz-option').forEach(el => {
    el.style.pointerEvents = 'none';
  });

  // Highlight selected and correct options
  const selectedEl = document.getElementById(`quiz-opt-${optIdx}`);
  const correctEl = document.getElementById(`quiz-opt-${q.correctIndex}`);

  if (isCorrect) {
    selectedEl.classList.add('correct');
    document.getElementById(`opt-marker-${optIdx}`).textContent = '✓ Correct';
    quizScore++;
  } else {
    selectedEl.classList.add('incorrect');
    document.getElementById(`opt-marker-${optIdx}`).textContent = '✗ Incorrect';
    correctEl.classList.add('correct');
    document.getElementById(`opt-marker-${q.correctIndex}`).textContent = '✓ Correct Answer';
  }

  userAnswers.push({
    questionId: q.id,
    selected: optIdx,
    correct: q.correctIndex,
    isCorrect: isCorrect
  });

  // Display Explanation
  const expBox = document.getElementById('quiz-explanation-box');
  document.getElementById('quiz-explanation-text').textContent = q.explanation;
  expBox.style.display = 'block';

  // Show Next / Finish Button
  const nextBtn = document.getElementById('quiz-next-btn');
  nextBtn.style.display = 'inline-flex';
  if (currentQuestionIndex === QUIZ_QUESTIONS.length - 1) {
    nextBtn.textContent = 'View Final Results ➔';
  } else {
    nextBtn.textContent = 'Next Question ➔';
  }
}

function handleQuizNext() {
  if (currentQuestionIndex < QUIZ_QUESTIONS.length - 1) {
    loadQuestion(currentQuestionIndex + 1);
  } else {
    finishQuiz();
  }
}

async function finishQuiz() {
  document.getElementById('quiz-active-card').style.display = 'none';
  document.getElementById('quiz-results-card').style.display = 'block';

  const total = QUIZ_QUESTIONS.length;
  const pct = Math.round((quizScore / total) * 100);

  document.getElementById('quiz-final-score').textContent = `${quizScore} / ${total}`;
  document.getElementById('quiz-final-percentage').textContent = `${pct}% Accuracy`;

  let badge = "Cybersecurity Apprentice";
  let summary = "Good initial start! Review the learning hub modules to strengthen your verification skills.";
  if (pct >= 90) {
    badge = "Master Fact-Checker & Cyber Sentinel 🛡️";
    summary = "Exceptional performance! You possess advanced critical thinking and forensic awareness against online deception.";
  } else if (pct >= 70) {
    badge = "Proficient Digital Investigator 🔍";
    summary = "Solid grasp of verification concepts and scam taxonomy. A few technical nuances warrant review.";
  }

  document.getElementById('quiz-achievement-badge').textContent = badge;
  document.getElementById('quiz-summary-text').textContent = summary;

  // Send anonymous result to backend for live metrics
  try {
    await fetch('/api/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ score: quizScore, total: total })
    });
  } catch (err) {
    console.warn('Could not log quiz completion:', err);
  }
}

window.resetQuizState = resetQuizState;
window.startQuiz = startQuiz;
window.selectQuizAnswer = selectQuizAnswer;
window.handleQuizNext = handleQuizNext;
