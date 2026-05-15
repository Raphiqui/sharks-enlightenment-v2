import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import ScrollIndicator from "../components/ScrollIndicator.vue";

describe("ScrollIndicator", () => {
  it("renders an svg arrow", () => {
    const wrapper = mount(ScrollIndicator);
    expect(wrapper.find("svg").exists()).toBe(true);
  });

  it("is clickable", () => {
    const wrapper = mount(ScrollIndicator);
    expect(wrapper.attributes("style")).toContain("cursor: pointer");
  });
});
