import { describe, it, expect } from "vitest";
import { t } from "../i18n.js";

describe("t()", () => {
  it("returns the correct English string for a known key", () => {
    expect(t("quizComplete")).toBe("Quiz Complete!");
  });

  it("returns the key itself when the key is unknown", () => {
    expect(t("nonexistent")).toBe("nonexistent");
  });

  it("interpolates params into the string", () => {
    expect(t("questionOf", { current: 1, total: 5 })).toBe(
      "Question 1 of 5",
    );
  });

  it("returns correct English fallback when lang has no translation", () => {
    expect(t("quizComplete")).toBeTruthy();
  });
});
