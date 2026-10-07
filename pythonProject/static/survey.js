const form = document.querySelector("#survey-form");
const errorBox = document.querySelector("#form-error");
const successPanel = document.querySelector("#success-panel");
const feedback = document.querySelector("#feedback");
const characterCount = document.querySelector("#character-count");
const submitButton = form.querySelector('button[type="submit"]');
const requiredFields = [
  "understanding_rating",
  "resolution_rating",
  "wait_time_rating",
];

feedback.addEventListener("input", () => {
  characterCount.textContent = feedback.value.length;
});

form.addEventListener("change", (event) => {
  const card = event.target.closest(".question-card");
  if (card) {
    card.classList.remove("invalid");
  }
  errorBox.hidden = true;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.hidden = true;

  const formData = new FormData(form);
  const missingFields = requiredFields.filter((field) => !formData.get(field));

  document.querySelectorAll(".question-card.invalid").forEach((card) => {
    card.classList.remove("invalid");
  });

  if (missingFields.length) {
    missingFields.forEach((field) => {
      form.querySelector(`input[name="${field}"]`).closest(".question-card").classList.add("invalid");
    });
    errorBox.textContent = "כדי לשלוח את הסקר, יש לענות על כל שאלות החובה.";
    errorBox.hidden = false;
    form.querySelector(".question-card.invalid").scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
    return;
  }

  const payload = {
    understanding_rating: Number(formData.get("understanding_rating")),
    resolution_rating: Number(formData.get("resolution_rating")),
    wait_time_rating: Number(formData.get("wait_time_rating")),
    feedback: formData.get("feedback"),
  };

  submitButton.disabled = true;
  submitButton.querySelector("span").textContent = "שולחים...";

  try {
    const response = await fetch("/api/survey", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "לא הצלחנו לשמור את הסקר.");
    }

    form.hidden = true;
    successPanel.hidden = false;
    successPanel.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch (error) {
    errorBox.textContent = error.message || "אירעה שגיאה. כדאי לנסות שוב בעוד רגע.";
    errorBox.hidden = false;
    submitButton.disabled = false;
    submitButton.querySelector("span").textContent = "שליחת הסקר";
  }
});
