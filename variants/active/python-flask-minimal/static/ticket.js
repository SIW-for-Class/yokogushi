(async function () {
  const root = document.getElementById("ticket");
  if (!root) return;

  const id = root.dataset.id;
  const btn = document.getElementById("toggle");
  const statusEl = document.getElementById("status");

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    try {
      const res = await fetch(`/api/tickets/${id}/toggle`, { method: "POST" });
      if (!res.ok) {
        alert(`エラー: ${res.status}`);
        return;
      }
      const data = await res.json();
      if (!data.ok) {
        alert("失敗しました");
        return;
      }

      // 表示更新（最小）
      statusEl.textContent = data.status;
      statusEl.classList.remove("open", "closed");
      statusEl.classList.add(data.status);
    } finally {
      btn.disabled = false;
    }
  });
})();

