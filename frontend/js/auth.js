// ==========================================
// MINEWISE AI - AUTHENTICATION
// ==========================================

// ==========================================
// LOGIN
// ==========================================

document.addEventListener(
  "DOMContentLoaded",

  () => {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
      loginForm.addEventListener(
        "submit",

        async (event) => {
          event.preventDefault();

          const email = document.getElementById("loginEmail").value.trim();

          const password = document.getElementById("loginPassword").value;

          try {
            await window.MOILAPI.login(
              email,

              password,
            );

            window.location.href = "dashboard.html";
          } catch (error) {
            alert("Login failed: " + error.message);
          }
        },
      );
    }

    // ==================================
    // REGISTER
    // ==================================

    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
      registerForm.addEventListener(
        "submit",

        async (event) => {
          event.preventDefault();

          const inputs = registerForm.querySelectorAll("input");

          const name = inputs[0].value.trim();

          const email = inputs[1].value.trim();

          const department = registerForm.querySelector("select").value;

          // Demo password for prototype

          const password = "Demo@123";

          try {
            await window.MOILAPI.register(
              name,

              email,

              password,

              "industrialist",
            );

            alert("Registration successful!\n\n" + "Department: " + department);

            window.location.href = "dashboard.html";
          } catch (error) {
            alert("Registration failed: " + error.message);
          }
        },
      );
    }
  },
);

// ==========================================
// QUICK DEMO ACCESS
// ==========================================

async function demoLogin() {
  try {
    await window.MOILAPI.login(
      "industrialist@moil.demo",

      "demo1234",
    );

    window.location.href = "dashboard.html";
  } catch (error) {
    console.error("Demo login failed:", error);

    alert("Demo login failed: " + error.message);
  }
}

// ==========================================
// MAKE FUNCTION AVAILABLE TO HTML
// ==========================================

window.demoLogin = demoLogin;
