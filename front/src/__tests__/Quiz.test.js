import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import QuizContainer from "../components/QuizContainer.vue";

const mockQuestions = [
  {
    id: 0,
    question: "What is the largest fish species?",
    options: [
      { option: "Whale shark", is_correct: true },
      { option: "Great white shark", is_correct: false },
    ],
    explanation: "The whale shark is the largest fish species.",
  },
  {
    id: 1,
    question: "Are sharks mammals?",
    options: [
      { option: "Yes", is_correct: false },
      { option: "No", is_correct: true },
    ],
    explanation: "Sharks are fish, not mammals.",
  },
];

class IntersectionObserverStub {
  observe() {}
  unobserve() {}
  disconnect() {}
}

async function mountQuiz(questions = mockQuestions) {
  global.fetch = vi.fn().mockResolvedValue({
    json: () => Promise.resolve({ questions }),
  });
  const wrapper = mount(QuizContainer);
  await flushPromises();
  return wrapper;
}

describe("Quiz", () => {
  beforeEach(() => {
    global.IntersectionObserver = IntersectionObserverStub;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("fetches questions from /api/quiz and renders the first question", async () => {
    const wrapper = await mountQuiz();

    expect(global.fetch).toHaveBeenCalledWith("/api/quiz");
    expect(wrapper.text()).toContain("What is the largest fish species?");
    expect(wrapper.findAll(".sq-option")).toHaveLength(2);
  });

  it("selecting the correct answer increments the score and reveals the explanation", async () => {
    const wrapper = await mountQuiz();

    const options = wrapper.findAll(".sq-option");
    await options[0].trigger("click");

    expect(options[0].classes()).toContain("option--correct");
    expect(wrapper.text()).toContain("The whale shark is the largest fish species.");
    expect(wrapper.text()).toContain("1 correct");
  });

  it("selecting a wrong answer marks it wrong and highlights the correct option", async () => {
    const wrapper = await mountQuiz();

    const options = wrapper.findAll(".sq-option");
    await options[1].trigger("click");

    expect(options[1].classes()).toContain("option--wrong");
    expect(options[0].classes()).toContain("option--correct");
    expect(wrapper.text()).toContain("0 correct");
  });

  it("ignores further clicks once a question has been answered", async () => {
    const wrapper = await mountQuiz();

    const options = wrapper.findAll(".sq-option");
    await options[1].trigger("click");
    await options[0].trigger("click");

    // Still wrong: the first click should be the one that counted.
    expect(options[1].classes()).toContain("option--wrong");
    expect(wrapper.text()).toContain("0 correct");
  });

  it("advances to the next question after clicking Next Question", async () => {
    const wrapper = await mountQuiz();

    await wrapper.findAll(".sq-option")[0].trigger("click");
    await wrapper.find(".sq-btn--next").trigger("click");

    expect(wrapper.text()).toContain("Are sharks mammals?");
    expect(wrapper.text()).toContain("Question 2 of 2");
  });

  it("shows the results panel with the final score after the last question", async () => {
    const wrapper = await mountQuiz();

    await wrapper.findAll(".sq-option")[0].trigger("click"); // correct
    await wrapper.find(".sq-btn--next").trigger("click");
    await wrapper.findAll(".sq-option")[1].trigger("click"); // correct
    await wrapper.find(".sq-btn--next").trigger("click");

    expect(wrapper.find(".sq-results").exists()).toBe(true);
    expect(wrapper.text()).toContain("Quiz Complete!");
    expect(wrapper.text()).toContain("100%");
  });

  it("restarts the quiz from the results panel", async () => {
    const wrapper = await mountQuiz();

    await wrapper.findAll(".sq-option")[0].trigger("click");
    await wrapper.find(".sq-btn--next").trigger("click");
    await wrapper.findAll(".sq-option")[1].trigger("click");
    await wrapper.find(".sq-btn--next").trigger("click");
    await wrapper.find(".sq-btn--restart").trigger("click");

    expect(wrapper.find(".sq-results").exists()).toBe(false);
    expect(wrapper.text()).toContain("What is the largest fish species?");
    expect(wrapper.text()).toContain("0 correct");
  });
});
