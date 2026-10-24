/**
 * EcoPulse Ultimate Hub - Client-Side Controller
 * Team Invicta Chaos: Sneha, Aditi, Divyanshi & Panchmi
 */

// Global State
let currentTab = 'dashboard';
let audioCtx = null;
let activeAudioSource = null;
let activeAudioFilter = null;
let activeAudioGain = null;
let currentPlayingSound = null;
let breathingInterval = null;
let focusLockInterval = null;

// Book Reading State
let booksData = [];
let currentBookId = 'alice';
let currentBookPage = 1;

// =========================================================
// 1. INITIALIZATION & THEME LOGIC
// =========================================================
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initClock();
    initSliders();
    initPillSelectors();
    initCanvas();
    initBooksReader();
    initMemoryGame();
    initSpeedMath();
    initRiddle();
    initKeyboardShortcuts();
});

function initTheme() {
    const savedTheme = localStorage.getItem('ecopulse_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('ecopulse_theme', next);
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    const btn = document.getElementById('themeToggleBtn');
    if (btn) {
        btn.innerHTML = theme === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
    }
}

function initClock() {
    const clockEl = document.getElementById('liveClock');
    if (!clockEl) return;
    const updateTime = () => {
        const now = new Date();
        clockEl.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    };
    updateTime();
    setInterval(updateTime, 1000);
}

// Tab Switcher
function switchTab(tabId) {
    document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

    const targetPanel = document.getElementById(tabId);
    if (targetPanel) {
        targetPanel.classList.add('active');
        currentTab = tabId;
    }

    const targetBtn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
    if (targetBtn) {
        targetBtn.classList.add('active');
    }
}

// Sliders value synchronization
function initSliders() {
    const bindSlider = (sliderId, displayId, suffix = '') => {
        const slider = document.getElementById(sliderId);
        const display = document.getElementById(displayId);
        if (slider && display) {
            slider.addEventListener('input', (e) => {
                display.innerText = `${e.target.value}${suffix}`;
            });
        }
    };

    bindSlider('sleepInput', 'sleepVal', 'h');
    bindSlider('screenInput', 'screenVal', 'h');
    bindSlider('stressInput', 'stressVal', '/10');
    bindSlider('commuteInput', 'commuteVal', ' km');
}

// Interactive Pill Selectors
function initPillSelectors() {
    document.querySelectorAll('.pill-selector').forEach(selector => {
        const hiddenInputId = selector.getAttribute('data-for');
        const hiddenInput = document.getElementById(hiddenInputId);
        selector.querySelectorAll('.pill-option').forEach(option => {
            option.addEventListener('click', () => {
                selector.querySelectorAll('.pill-option').forEach(o => o.classList.remove('active'));
                option.classList.add('active');
                if (hiddenInput) {
                    hiddenInput.value = option.getAttribute('data-value');
                }
            });
        });
    });
}

function initKeyboardShortcuts() {
    window.addEventListener('keydown', (e) => {
        if (currentTab === 'books') {
            if (e.key === 'ArrowRight') {
                changeBookPage(1);
            } else if (e.key === 'ArrowLeft') {
                changeBookPage(-1);
            }
        }
    });
}

// =========================================================
// 2. DIAGNOSTIC AJAX HANDLER (No Page Reloads)
// =========================================================
async function submitDiagnostic(event) {
    if (event) event.preventDefault();

    const form = document.getElementById('diagnosticForm');
    const formData = new FormData(form);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();
        if (data.success) {
            renderDiagnosticResults(data.results);
            updateProfileUI(data.profile);
            showToast(`🚀 Diagnostic synced! +${data.results.earned_xp} XP awarded!`);
            
            const resultsBox = document.getElementById('resultsDashboard');
            if (resultsBox) {
                resultsBox.scrollIntoView({ behavior: 'smooth' });
            }
        }
    } catch (err) {
        console.error("Diagnostic submission error:", err);
        if (form) form.submit();
    }
}

function renderDiagnosticResults(res) {
    const box = document.getElementById('resultsDashboard');
    if (!box) return;

    box.style.display = 'block';

    const riskBadge = document.getElementById('resultRiskBadge');
    if (riskBadge) {
        riskBadge.className = `badge bg-${res.burnout_class}`;
        riskBadge.innerText = `${res.burnout_risk} Risk (${res.burnout_score}/100)`;
    }

    const burnoutMsg = document.getElementById('resultBurnoutMsg');
    if (burnoutMsg) burnoutMsg.innerText = res.burnout_msg;

    const co2Total = document.getElementById('resultCo2Total');
    if (co2Total) co2Total.innerText = `${res.co2_total} kg CO₂`;

    const co2Subtext = document.getElementById('resultCo2Subtext');
    if (co2Subtext) co2Subtext.innerText = `~${res.laptop_charges} laptop charges | ~${res.phone_charges} smartphone charges`;

    const co2Saved = document.getElementById('resultCo2Saved');
    if (co2Saved) co2Saved.innerText = `🌿 You saved ~${res.co2_saved} kg CO₂ vs high-emission baseline today!`;

    // Tailored Workout
    const workoutContainer = document.getElementById('resultWorkoutCard');
    if (workoutContainer) {
        workoutContainer.innerHTML = `
            <h4>🏃 Tailored Movement: ${res.workout.name}</h4>
            <div style="font-size:0.82rem; color:var(--primary-light); font-weight:700; margin-bottom:4px;">
                ${res.workout.type} | Duration: ${res.workout.duration} | Space: ${res.workout.equipment}
            </div>
            <p>${res.workout.desc}</p>
            <button class="quick-water-btn" style="margin-top:8px; width:auto;" onclick="logSpecificWorkout('${res.workout.name}', '${res.workout.type}', '${res.workout.duration}', '${res.workout.equipment}', 'Moderate', 60)">
                ✅ Log Workout (+35 XP)
            </button>
        `;
    }

    // Tailored Recipe
    const recipeContainer = document.getElementById('resultRecipeCard');
    if (recipeContainer) {
        recipeContainer.innerHTML = `
            <h4>${res.recipe.title}</h4>
            <div style="font-size:0.82rem; color:var(--eco-green); font-weight:700; margin-bottom:4px;">
                ${res.recipe.category} | ${res.recipe.time} | ${res.recipe.calories} | ${res.recipe.protein}
            </div>
            <p>${res.recipe.instructions}</p>
            <div style="margin-top:6px; font-size:0.85rem; color:var(--primary);"><strong>Impact:</strong> ${res.recipe.co2}</div>
        `;
    }

    // Custom Interventions List
    const interContainer = document.getElementById('resultInterventionsList');
    if (interContainer) {
        interContainer.innerHTML = res.interventions.map(item => `
            <div class="solution-item">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4>${item.title}</h4>
                    <span class="badge" style="background:var(--eco-green); font-size:0.75rem;">${item.badge}</span>
                </div>
                <p style="margin-top:6px;">${item.desc}</p>
            </div>
        `).join('');
    }
}

// =========================================================
// 3. GAMIFICATION & HYDRATION REAL-TIME SYNC
// =========================================================
function updateProfileUI(profile) {
    if (!profile) return;

    const streakEl = document.getElementById('streakVal');
    if (streakEl) streakEl.innerText = `🔥 ${profile.streak_days} Days`;

    const xpEl = document.getElementById('totalXpVal');
    if (xpEl) xpEl.innerText = `⭐ ${profile.total_xp} XP`;

    const levelTitleEl = document.getElementById('levelTitleVal');
    if (levelTitleEl) levelTitleEl.innerText = `Lvl ${profile.level}: ${profile.level_title}`;

    const xpBar = document.getElementById('xpProgressFill');
    if (xpBar) xpBar.style.width = `${profile.xp_percent}%`;

    const plantStageEl = document.getElementById('plantStageVal');
    if (plantStageEl) plantStageEl.innerText = profile.plant_stage;

    const bottlesEl = document.getElementById('bottlesSavedVal');
    if (bottlesEl) bottlesEl.innerText = `💧 ${profile.bottles_saved}`;

    const co2El = document.getElementById('co2SavedVal');
    if (co2El) co2El.innerText = `🌿 ${profile.total_co2_saved} kg`;

    const waterCounter = document.getElementById('waterCountPill');
    if (waterCounter) waterCounter.innerText = `${profile.glasses_drank_today || 5} Glasses`;
}

async function quickDrinkWater() {
    try {
        const res = await fetch('/api/water/drink', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            updateProfileUI(data.profile);
            showToast(data.message);
            playTone(520, 0.15, 'sine');
        }
    } catch (e) {
        console.error(e);
    }
}

async function claimDailyQuest(questId) {
    try {
        const res = await fetch('/api/quests/claim', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ quest_id: questId })
        });
        const data = await res.json();
        if (data.success) {
            updateProfileUI(data.profile);
            showToast(`🎉 Quest Completed! +${data.awarded_xp} XP earned!`);
            const btn = document.getElementById(`quest-btn-${questId}`);
            if (btn) {
                btn.disabled = true;
                btn.innerText = "Completed ✅";
                btn.style.background = "var(--border-color)";
                btn.style.color = "var(--text-muted)";
            }
        } else {
            showToast("Quest already claimed or in progress!");
        }
    } catch (e) {
        console.error(e);
    }
}

// =========================================================
// 4. WORKOUT TRACKER & WORKOUT STREAK LOGGING
// =========================================================
async function logSpecificWorkout(name, type, duration, equipment, intensity, calories) {
    try {
        const res = await fetch('/api/workout/log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                workout_name: name,
                workout_type: type || 'Strength',
                duration: duration || '10 Mins',
                equipment: equipment || 'Bodyweight',
                intensity: intensity || 'Moderate Strength',
                calories: calories || 60,
                xp: 35
            })
        });

        const data = await res.json();
        if (data.success) {
            updateProfileUI(data.profile);
            updateWorkoutStatsUI(data.stats);
            renderWorkoutLogsTable(data.logs);
            showToast(data.message);
            playTone(580, 0.2, 'triangle');
        }
    } catch (e) {
        console.error("Workout logging error:", e);
    }
}

async function logCustomWorkout() {
    const nameInput = document.getElementById('customWorkoutName');
    const typeSelect = document.getElementById('customWorkoutType');
    const durInput = document.getElementById('customWorkoutDuration');

    const name = nameInput ? nameInput.value.trim() : '';
    if (!name) {
        showToast("⚠️ Please enter a workout name (e.g. Campus Morning Jog)");
        return;
    }

    const type = typeSelect ? typeSelect.value : 'Cardio';
    const duration = durInput ? durInput.value.trim() : '15 Mins';

    await logSpecificWorkout(name, type, duration, 'Custom', 'Moderate', 80);
    if (nameInput) nameInput.value = '';
}

async function deleteWorkoutItem(logId) {
    if (!confirm("Are you sure you want to remove this workout entry?")) return;

    try {
        const res = await fetch(`/api/workout/${logId}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            updateWorkoutStatsUI(data.stats);
            renderWorkoutLogsTable(data.logs);
            updateProfileUI(data.profile);
            showToast("Workout log removed.");
        }
    } catch (e) {
        console.error(e);
    }
}

function updateWorkoutStatsUI(stats) {
    if (!stats) return;
    const streakEl = document.getElementById('workoutStreakVal');
    if (streakEl) streakEl.innerText = `🔥 ${stats.streak} Days`;

    const totalEl = document.getElementById('totalWorkoutsVal');
    if (totalEl) totalEl.innerText = `🏋️ ${stats.total_workouts}`;

    const calEl = document.getElementById('totalWorkoutCaloriesVal');
    if (calEl) calEl.innerText = `⚡ ${stats.total_calories} kcal`;

    const xpEl = document.getElementById('totalWorkoutXpVal');
    if (xpEl) xpEl.innerText = `⭐ ${stats.total_xp} XP`;
}

function renderWorkoutLogsTable(logs) {
    const tbody = document.getElementById('workoutHistoryBody');
    if (!tbody || !logs) return;

    if (logs.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" style="text-align:center; padding:16px; color:var(--text-muted);">
                    No workouts logged yet. Complete a workout routine above to start your streak!
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = logs.map(w => `
        <tr id="workout-row-${w.id}">
            <td>${w.timestamp}</td>
            <td><strong>${w.workout_name}</strong></td>
            <td>${w.workout_type}</td>
            <td>${w.duration}</td>
            <td>${w.intensity}</td>
            <td>${w.calories_est} kcal</td>
            <td><strong style="color:var(--teal-light);">+${w.xp_earned}</strong></td>
            <td>
                <button class="btn-secondary" style="padding:2px 8px; font-size:0.75rem; color:var(--coral-red);" onclick="deleteWorkoutItem(${w.id})">
                    🗑️
                </button>
            </td>
        </tr>
    `).join('');
}

// =========================================================
// 5. BOOK LOVERS HAVEN (Multi-Page Navigation Engine)
// =========================================================
function initBooksReader() {
    const jsonEl = document.getElementById('booksDataJson');
    if (jsonEl) {
        try {
            booksData = JSON.parse(jsonEl.textContent);
        } catch (e) {
            console.error("Error loading books data JSON:", e);
        }
    }

    if (booksData && booksData.length > 0) {
        currentBookId = booksData[0].id;
        currentBookPage = 1;
        renderBookPage();
    }
}

function selectBook(bookId) {
    currentBookId = bookId;
    currentBookPage = 1;

    document.querySelectorAll('.book-btn').forEach(btn => {
        if (btn.getAttribute('data-book') === bookId) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    renderBookPage();
    showToast("📖 Book loaded. You can flip pages using ⬅️ / ➡️ or arrow keys!");
}

function changeBookPage(delta) {
    const book = booksData.find(b => b.id === currentBookId);
    if (!book || !book.pages) return;

    const totalPages = book.pages.length;
    const newPage = currentBookPage + delta;

    if (newPage < 1 || newPage > totalPages) return;

    currentBookPage = newPage;
    renderBookPage();

    // If moving forward, save progress & award XP
    if (delta > 0) {
        saveReadingProgressOnServer(currentBookId, currentBookPage);
    }
}

function renderBookPage() {
    const book = booksData.find(b => b.id === currentBookId);
    if (!book || !book.pages) return;

    const pageIndex = currentBookPage - 1;
    const pageData = book.pages[pageIndex] || book.pages[0];
    const totalPages = book.pages.length;

    const chapterTitleEl = document.getElementById('bookChapterTitle');
    if (chapterTitleEl) chapterTitleEl.innerText = pageData.title;

    const contentEl = document.getElementById('bookPageContent');
    if (contentEl) contentEl.innerText = pageData.text;

    const topIndicator = document.getElementById('pageIndicatorTop');
    if (topIndicator) topIndicator.innerText = `Page ${currentBookPage} of ${totalPages}`;

    const bottomIndicator = document.getElementById('pageIndicatorBottom');
    if (bottomIndicator) bottomIndicator.innerText = `Page ${currentBookPage} of ${totalPages}`;

    const progressBar = document.getElementById('readingProgressBar');
    if (progressBar) {
        const pct = (currentBookPage / totalPages) * 100;
        progressBar.style.width = `${pct}%`;
    }

    // Toggle disabled state on buttons
    const prevTop = document.getElementById('prevPageTopBtn');
    const prevBottom = document.getElementById('prevPageBottomBtn');
    const nextTop = document.getElementById('nextPageTopBtn');
    const nextBottom = document.getElementById('nextPageBottomBtn');

    if (prevTop) prevTop.disabled = currentBookPage <= 1;
    if (prevBottom) prevBottom.disabled = currentBookPage <= 1;
    if (nextTop) nextTop.disabled = currentBookPage >= totalPages;
    if (nextBottom) nextBottom.disabled = currentBookPage >= totalPages;
}

async function saveReadingProgressOnServer(bookId, pageNum) {
    try {
        const res = await fetch('/api/reading/progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ book_id: bookId, page_num: pageNum })
        });
        const data = await res.json();
        if (data.success && data.profile) {
            updateProfileUI(data.profile);
            playTone(480, 0.1, 'sine');
            showToast(data.message);
        }
    } catch (e) {
        console.error(e);
    }
}

let currentFontSize = 1.1;
function adjustBookFontSize(delta) {
    currentFontSize = Math.max(0.85, Math.min(1.6, currentFontSize + delta));
    const readerEl = document.getElementById('bookReaderDisplay');
    if (readerEl) {
        readerEl.style.fontSize = `${currentFontSize}rem`;
    }
}

function toggleReaderTheme(mode) {
    const readerEl = document.getElementById('bookReaderDisplay');
    if (!readerEl) return;
    readerEl.className = `reader-container ${mode}-theme`;
}

// =========================================================
// 6. DOODLE CANVAS & GALLERY SYSTEM
// =========================================================
let canvas, ctx, drawing = false;
let canvasUndoHistory = [];
let canvasRedoHistory = [];
let isEraserMode = false;

function initCanvas() {
    canvas = document.getElementById('doodleCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    const resize = () => {
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        saveCanvasState();
    };
    resize();
    window.addEventListener('resize', resize);

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseleave', stopDrawing);

    // Touch support for tablets/mobile
    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousedown', { clientX: touch.clientX, clientY: touch.clientY });
        canvas.dispatchEvent(mouseEvent);
    });
    canvas.addEventListener('touchend', (e) => {
        const mouseEvent = new MouseEvent('mouseup', {});
        canvas.dispatchEvent(mouseEvent);
    });
    canvas.addEventListener('touchmove', (e) => {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousemove', { clientX: touch.clientX, clientY: touch.clientY });
        canvas.dispatchEvent(mouseEvent);
    });
}

function startDrawing(e) {
    drawing = true;
    canvasRedoHistory = []; // Reset redo on new stroke
    draw(e);
}

function stopDrawing() {
    if (drawing) {
        drawing = false;
        ctx.beginPath();
        saveCanvasState();
    }
}

function draw(e) {
    if (!drawing) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const brushColor = isEraserMode ? "#ffffff" : document.getElementById('brushColor').value;
    const brushSize = document.getElementById('brushSize').value;

    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = brushColor;

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

function saveCanvasState() {
    if (canvas && canvasUndoHistory.length < 25) {
        canvasUndoHistory.push(canvas.toDataURL());
    }
}

function undoCanvas() {
    if (canvasUndoHistory.length > 1) {
        canvasRedoHistory.push(canvasUndoHistory.pop());
        const prevState = canvasUndoHistory[canvasUndoHistory.length - 1];
        const img = new Image();
        img.src = prevState;
        img.onload = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
        };
    }
}

function redoCanvas() {
    if (canvasRedoHistory.length > 0) {
        const nextState = canvasRedoHistory.pop();
        canvasUndoHistory.push(nextState);
        const img = new Image();
        img.src = nextState;
        img.onload = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
        };
    }
}

function clearCanvas() {
    if (ctx && canvas) {
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        saveCanvasState();
        showToast("Canvas cleared.");
    }
}

function setBrushPreset(color) {
    isEraserMode = false;
    updateEraserBtnState();
    const input = document.getElementById('brushColor');
    if (input) input.value = color;
}

function toggleEraser() {
    isEraserMode = !isEraserMode;
    updateEraserBtnState();
    showToast(isEraserMode ? "🧹 Eraser tool active" : "✏️ Brush tool active");
}

function updateEraserBtnState() {
    const btn = document.getElementById('eraserToggleBtn');
    if (!btn) return;
    if (isEraserMode) {
        btn.style.background = "var(--amber)";
        btn.style.color = "white";
    } else {
        btn.style.background = "";
        btn.style.color = "";
    }
}

function downloadCanvas() {
    if (!canvas) return;
    const link = document.createElement('a');
    link.download = `ecopulse-doodle-${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    showToast("🎨 Doodle downloaded to your computer!");
}

async function saveCurrentDoodle() {
    if (!canvas) return;

    const titleInput = document.getElementById('doodleTitleInput');
    const authorInput = document.getElementById('doodleAuthorInput');

    const title = titleInput && titleInput.value.trim() ? titleInput.value.trim() : "Dorm Canvas Sketch";
    const author = authorInput && authorInput.value.trim() ? authorInput.value.trim() : "Anonymous Artist";
    const dataUrl = canvas.toDataURL('image/png');

    try {
        const res = await fetch('/api/doodles', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ author, title, image_data: dataUrl })
        });
        const data = await res.json();
        if (data.success) {
            updateProfileUI(data.profile);
            showToast(data.message);
            renderGalleryDoodles(data.doodles);
            if (titleInput) titleInput.value = '';
            if (authorInput) authorInput.value = '';
        }
    } catch (e) {
        console.error(e);
    }
}

function renderGalleryDoodles(doodles) {
    const container = document.getElementById('communityDoodlesGallery');
    if (!container || !doodles) return;

    if (doodles.length === 0) {
        container.innerHTML = `<p style="font-size:0.85rem; color:var(--text-muted); font-style:italic;">No doodles saved yet. Draw above and click Save to Gallery!</p>`;
        return;
    }

    container.innerHTML = doodles.map(d => `
        <div class="doodle-card" id="doodle-card-${d.id}">
            <img src="${d.image_data}" class="doodle-thumb" alt="${d.title}">
            <div style="font-weight:750; font-size:0.85rem; margin-top:6px; color:var(--text-primary);">${d.title}</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">by ${d.author} • ${d.timestamp}</div>
            <div class="doodle-actions">
                <button class="btn-secondary" style="font-size:0.75rem; padding:3px 8px;" onclick="loadDoodleOntoCanvas('${d.id}')">✏️ Edit</button>
                <button class="btn-secondary" style="font-size:0.75rem; padding:3px 8px;" onclick="downloadDoodleDirect('${d.image_data}', '${d.title}')">📥 Save</button>
                <button class="btn-secondary" style="font-size:0.75rem; padding:3px 8px; color:var(--coral-red);" onclick="deleteDoodleItem('${d.id}')">🗑️</button>
            </div>
        </div>
    `).join('');
}

async function loadDoodleOntoCanvas(doodleId) {
    try {
        const res = await fetch(`/api/doodles/${doodleId}`);
        const data = await res.json();
        if (data.success && data.doodle) {
            const img = new Image();
            img.src = data.doodle.image_data;
            img.onload = () => {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                saveCanvasState();
                showToast(`🎨 "${data.doodle.title}" loaded onto canvas! You can continue drawing.`);
                canvas.scrollIntoView({ behavior: 'smooth' });
            };
        }
    } catch (e) {
        console.error(e);
    }
}

function downloadDoodleDirect(dataUrl, title) {
    const link = document.createElement('a');
    link.download = `${title.toLowerCase().replace(/\\s+/g, '-')}-${Date.now()}.png`;
    link.href = dataUrl;
    link.click();
    showToast("🎨 Doodle downloaded!");
}

async function deleteDoodleItem(doodleId) {
    if (!confirm("Are you sure you want to delete this doodle from your gallery?")) return;

    try {
        const res = await fetch(`/api/doodles/${doodleId}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            renderGalleryDoodles(data.doodles);
            updateProfileUI(data.profile);
            showToast("Doodle deleted.");
        }
    } catch (e) {
        console.error(e);
    }
}

// =========================================================
// 7. STUDENT LITERARY CORNER (NO Member Names)
// =========================================================
async function submitLiteraryPost(event) {
    if (event) event.preventDefault();
    const form = document.getElementById('literaryForm');
    const formData = new FormData(form);

    try {
        const res = await fetch('/api/literary', {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();
        if (data.success) {
            updateProfileUI(data.profile);
            showToast("✍️ Literary piece published! +35 XP awarded!");
            form.reset();
            renderLiteraryPosts(data.posts);
        }
    } catch (e) {
        console.error(e);
    }
}

async function likeLiteraryPost(postId) {
    try {
        const res = await fetch(`/api/literary/${postId}/like`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            updateProfileUI(data.profile);
            const countEl = document.getElementById(`like-count-${postId}`);
            if (countEl) countEl.innerText = data.likes;
            playTone(600, 0.1, 'sine');
            showToast("❤️ Liked! +5 XP");
        }
    } catch(e) {
        console.error(e);
    }
}

function renderLiteraryPosts(posts) {
    const container = document.getElementById('literaryPostsContainer');
    if (!container || !posts) return;
    container.innerHTML = posts.map(post => `
        <div class="literary-post-card">
            <div class="post-header">
                <div>
                    <span class="post-author">${post.author}</span>
                    <span class="post-tag">${post.tag || 'Student Voice'}</span>
                </div>
                <button class="like-btn" onclick="likeLiteraryPost(${post.id})">
                    ❤️ <span id="like-count-${post.id}">${post.likes}</span>
                </button>
            </div>
            <h4 style="font-size:0.96rem; margin-bottom:4px;">${post.title}</h4>
            <p style="font-size:0.88rem; font-style:italic; color:var(--text-secondary); white-space:pre-wrap;">"${post.content}"</p>
            <div style="font-size:0.72rem; color:var(--text-muted); margin-top:6px;">${post.timestamp}</div>
        </div>
    `).join('');
}

// =========================================================
// 8. WEB AUDIO API SYNTHESIZER (100% Offline Ambient Sound Engine)
// =========================================================
function getAudioContext() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
    return audioCtx;
}

function playSynthSound(type) {
    stopSynthSound();
    const ctx = getAudioContext();
    const volumeSlider = document.getElementById('ambientVolume');
    const vol = volumeSlider ? parseFloat(volumeSlider.value) : 0.2;

    activeAudioGain = ctx.createGain();
    activeAudioGain.gain.setValueAtTime(vol, ctx.currentTime);
    activeAudioGain.connect(ctx.destination);

    currentPlayingSound = type;
    updateAudioButtonStates(type);

    if (type === 'rain' || type === 'waves' || type === 'wind' || type === 'brown') {
        const bufferSize = ctx.sampleRate * 4;
        const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const output = noiseBuffer.getChannelData(0);

        let lastOut = 0.0;
        for (let i = 0; i < bufferSize; i++) {
            const white = Math.random() * 2 - 1;
            if (type === 'brown') {
                output[i] = (lastOut + (0.02 * white)) / 1.02;
                lastOut = output[i];
                output[i] *= 3.5;
            } else {
                output[i] = white;
            }
        }

        const whiteNoise = ctx.createBufferSource();
        whiteNoise.buffer = noiseBuffer;
        whiteNoise.loop = true;

        activeAudioFilter = ctx.createBiquadFilter();

        if (type === 'rain') {
            activeAudioFilter.type = 'lowpass';
            activeAudioFilter.frequency.setValueAtTime(950, ctx.currentTime);
        } else if (type === 'waves') {
            activeAudioFilter.type = 'bandpass';
            activeAudioFilter.frequency.setValueAtTime(450, ctx.currentTime);
            activeAudioFilter.Q.setValueAtTime(3.0, ctx.currentTime);

            const lfo = ctx.createOscillator();
            const lfoGain = ctx.createGain();
            lfo.frequency.setValueAtTime(0.12, ctx.currentTime);
            lfoGain.gain.setValueAtTime(350, ctx.currentTime);
            lfo.connect(lfoGain);
            lfoGain.connect(activeAudioFilter.frequency);
            lfo.start();
        } else if (type === 'wind') {
            activeAudioFilter.type = 'bandpass';
            activeAudioFilter.frequency.setValueAtTime(650, ctx.currentTime);
            activeAudioFilter.Q.setValueAtTime(1.5, ctx.currentTime);
        } else if (type === 'brown') {
            activeAudioFilter.type = 'lowpass';
            activeAudioFilter.frequency.setValueAtTime(400, ctx.currentTime);
        }

        whiteNoise.connect(activeAudioFilter);
        activeAudioFilter.connect(activeAudioGain);
        whiteNoise.start();
        activeAudioSource = whiteNoise;

    } else if (type === 'chime') {
        const fundamental = 432;
        const osc1 = ctx.createOscillator();
        const osc2 = ctx.createOscillator();
        const chimeGain = ctx.createGain();

        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(fundamental, ctx.currentTime);
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(fundamental * 2.02, ctx.currentTime);

        chimeGain.gain.setValueAtTime(vol * 0.8, ctx.currentTime);
        chimeGain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 6.0);

        osc1.connect(chimeGain);
        osc2.connect(chimeGain);
        chimeGain.connect(ctx.destination);

        osc1.start();
        osc2.start();
        osc1.stop(ctx.currentTime + 6.0);
        osc2.stop(ctx.currentTime + 6.0);
    }
}

function stopSynthSound() {
    if (activeAudioSource) {
        try { activeAudioSource.stop(); } catch(e){}
        activeAudioSource = null;
    }
    if (activeAudioGain) {
        try { activeAudioGain.disconnect(); } catch(e){}
        activeAudioGain = null;
    }
    currentPlayingSound = null;
    updateAudioButtonStates(null);
}

function updateAudioButtonStates(activeType) {
    document.querySelectorAll('.sound-toggle-btn').forEach(btn => {
        const sound = btn.getAttribute('data-sound');
        if (sound === activeType) {
            btn.classList.add('playing');
        } else {
            btn.classList.remove('playing');
        }
    });
}

function setAmbientVolume(val) {
    if (activeAudioGain && audioCtx) {
        activeAudioGain.gain.setValueAtTime(parseFloat(val), audioCtx.currentTime);
    }
}

function playTone(freq, duration, wave = 'sine') {
    try {
        const ctx = getAudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = wave;
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        gain.gain.setValueAtTime(0.12, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + duration);
    } catch(e) {}
}

// 4-7-8 Breathing Meditation Circle
function startBreathing() {
    const circle = document.getElementById('breathingCircle');
    const text = document.getElementById('breathingText');
    const timer = document.getElementById('breathingCounter');
    if (!circle || !text) return;

    stopBreathing();

    let step = 0;
    let timeLeft = 4;

    const cycle = () => {
        if (step === 0) {
            circle.className = 'breathing-circle-outer inhale';
            text.innerText = 'Inhale';
            timeLeft = 4;
            playTone(440, 0.1, 'sine');
        } else if (step === 1) {
            circle.className = 'breathing-circle-outer hold';
            text.innerText = 'Hold';
            timeLeft = 7;
        } else if (step === 2) {
            circle.className = 'breathing-circle-outer exhale';
            text.innerText = 'Exhale';
            timeLeft = 8;
            playTone(330, 0.1, 'sine');
        }
    };

    cycle();
    breathingInterval = setInterval(() => {
        timeLeft--;
        if (timer) timer.innerText = `${timeLeft}s`;
        if (timeLeft <= 0) {
            step = (step + 1) % 3;
            cycle();
        }
    }, 1000);
}

function stopBreathing() {
    if (breathingInterval) {
        clearInterval(breathingInterval);
        breathingInterval = null;
    }
    const circle = document.getElementById('breathingCircle');
    const text = document.getElementById('breathingText');
    const timer = document.getElementById('breathingCounter');
    if (circle) circle.className = 'breathing-circle-outer';
    if (text) text.innerText = 'Ready';
    if (timer) timer.innerText = '4-7-8';
}

// Positive Quote Generator
const DEFAULT_QUOTES_LIST = [
    { quote: "The secret of getting ahead is getting started.", author: "Mark Twain" },
    { quote: "Small daily improvements over time lead to stunning results.", author: "Robin Sharma" },
    { quote: "In the middle of difficulty lies opportunity.", author: "Albert Einstein" },
    { quote: "Caring for yourself is caring for the planet. Every mindful choice echoes outward.", author: "EcoPulse" },
    { quote: "You don't have to be great to start, but you have to start to be great.", author: "Zig Ziglar" },
    { quote: "Rest when you're weary. Refresh and renew yourself, your body, your mind.", author: "Mindfulness Guide" },
    { quote: "The greatest threat to our planet is the belief that someone else will save it.", author: "Robert Swan" }
];

function generateNewQuote() {
    const q = DEFAULT_QUOTES_LIST[Math.floor(Math.random() * DEFAULT_QUOTES_LIST.length)];
    const quoteEl = document.getElementById('quoteDisplay');
    const authorEl = document.getElementById('quoteAuthor');
    if (quoteEl) quoteEl.innerText = `“${q.quote}”`;
    if (authorEl) authorEl.innerText = `— ${q.author}`;
    showToast("✨ New inspiration loaded!");
}

// =========================================================
// 9. BRAIN ARCADE & PUZZLES
// =========================================================
let currentMathPuzzle = null;
let currentRiddle = null;

async function initSpeedMath() {
    try {
        const res = await fetch('/api/puzzle/math');
        const data = await res.json();
        currentMathPuzzle = data;
        const display = document.getElementById('mathProblemText');
        if (display) display.innerText = `${data.question} = ?`;
        const ansInput = document.getElementById('mathAnswerInput');
        if (ansInput) ansInput.value = '';
        const feedback = document.getElementById('mathFeedbackText');
        if (feedback) feedback.innerText = '';
    } catch(e) {
        console.error(e);
    }
}

async function verifySpeedMath() {
    const ansInput = document.getElementById('mathAnswerInput');
    const feedback = document.getElementById('mathFeedbackText');
    if (!ansInput || !currentMathPuzzle) return;

    try {
        const res = await fetch('/api/puzzle/math/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentMathPuzzle.id, answer: ansInput.value })
        });
        const data = await res.json();
        if (data.correct) {
            feedback.style.color = "var(--eco-green)";
            feedback.innerText = `🎉 Correct! (+${data.earned_xp} Brain XP)! Loading next...`;
            updateProfileUI(data.profile);
            playTone(660, 0.2, 'triangle');
            setTimeout(initSpeedMath, 1200);
        } else {
            feedback.style.color = "var(--coral-red)";
            feedback.innerText = `❌ Not quite! The answer was ${data.expected}. Try another!`;
            playTone(220, 0.2, 'sawtooth');
            setTimeout(initSpeedMath, 1500);
        }
    } catch(e) {
        console.error(e);
    }
}

async function initRiddle() {
    try {
        const res = await fetch('/api/puzzle/riddle');
        const data = await res.json();
        currentRiddle = data;
        const riddleText = document.getElementById('riddleQuestionText');
        if (riddleText) riddleText.innerText = `"${data.riddle}"`;
        const hintText = document.getElementById('riddleHintText');
        if (hintText) {
            hintText.innerText = `💡 Hint: ${data.hint}`;
            hintText.style.display = 'none';
        }
        const guessInput = document.getElementById('riddleGuessInput');
        if (guessInput) guessInput.value = '';
        const feedback = document.getElementById('riddleFeedbackText');
        if (feedback) feedback.innerText = '';
    } catch(e) {
        console.error(e);
    }
}

function toggleRiddleHint() {
    const hintText = document.getElementById('riddleHintText');
    if (hintText) {
        hintText.style.display = hintText.style.display === 'none' ? 'block' : 'none';
    }
}

async function verifyRiddle() {
    const guessInput = document.getElementById('riddleGuessInput');
    const feedback = document.getElementById('riddleFeedbackText');
    if (!guessInput || !currentRiddle) return;

    try {
        const res = await fetch('/api/puzzle/riddle/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentRiddle.id, guess: guessInput.value })
        });
        const data = await res.json();
        if (data.correct) {
            feedback.style.color = "var(--eco-green)";
            feedback.innerText = `🎉 Brilliant deduction! The answer is ${data.answer.toUpperCase()} (+${data.earned_xp} XP)!`;
            updateProfileUI(data.profile);
            playTone(550, 0.25, 'sine');
            setTimeout(initRiddle, 2000);
        } else {
            feedback.style.color = "var(--coral-red)";
            feedback.innerText = "❌ Close guess! Try looking at the hint above.";
            playTone(240, 0.15, 'sine');
        }
    } catch(e) {
        console.error(e);
    }
}

// Memory Match Game
const MEMORY_EMOJIS = ['🌱', '💧', '🚲', '🥗', '🧘', '⚡'];
let memoryCards = [];
let memoryFlipped = [];
let memoryMatched = [];

function initMemoryGame() {
    const container = document.getElementById('memoryCardsGrid');
    if (!container) return;

    memoryCards = [...MEMORY_EMOJIS, ...MEMORY_EMOJIS].sort(() => 0.5 - Math.random());
    memoryFlipped = [];
    memoryMatched = [];

    container.innerHTML = memoryCards.map((emoji, index) => `
        <div class="memory-card" id="mem-card-${index}" onclick="flipMemoryCard(${index})">
            ❓
        </div>
    `).join('');
}

function flipMemoryCard(index) {
    if (memoryFlipped.length >= 2 || memoryFlipped.includes(index) || memoryMatched.includes(index)) return;

    const card = document.getElementById(`mem-card-${index}`);
    card.innerText = memoryCards[index];
    card.classList.add('revealed');
    memoryFlipped.push(index);

    if (memoryFlipped.length === 2) {
        const [idx1, idx2] = memoryFlipped;
        if (memoryCards[idx1] === memoryCards[idx2]) {
            memoryMatched.push(idx1, idx2);
            document.getElementById(`mem-card-${idx1}`).classList.add('matched');
            document.getElementById(`mem-card-${idx2}`).classList.add('matched');
            memoryFlipped = [];
            playTone(580, 0.15, 'sine');

            if (memoryMatched.length === memoryCards.length) {
                showToast("🎉 Memory Match Mastered! +30 Brain XP!");
                logSpecificWorkout("Memory Brain Challenge", "Mindfulness", "5 Mins", "None", "Low", 25);
            }
        } else {
            setTimeout(() => {
                document.getElementById(`mem-card-${idx1}`).innerText = '❓';
                document.getElementById(`mem-card-${idx2}`).innerText = '❓';
                document.getElementById(`mem-card-${idx1}`).classList.remove('revealed');
                document.getElementById(`mem-card-${idx2}`).classList.remove('revealed');
                memoryFlipped = [];
            }, 800);
        }
    }
}

// =========================================================
// 10. DIGITAL DETOX & DEEP FOCUS LOCK
// =========================================================
function startFocusLock() {
    const mins = parseInt(document.getElementById('lockMinutesInput').value) || 15;
    let totalSecs = mins * 60;
    const overlay = document.getElementById('lockOverlay');
    const timerDisplay = document.getElementById('lockTimerDisplay');

    if (!overlay || !timerDisplay) return;

    overlay.style.display = 'flex';
    clearInterval(focusLockInterval);

    focusLockInterval = setInterval(async () => {
        const m = Math.floor(totalSecs / 60);
        const s = totalSecs % 60;
        timerDisplay.innerText = `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;

        if (totalSecs <= 0) {
            clearInterval(focusLockInterval);
            overlay.style.display = 'none';
            try {
                const res = await fetch('/api/focus/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ minutes: mins })
                });
                const data = await res.json();
                if (data.success) {
                    updateProfileUI(data.profile);
                    showToast(data.message);
                }
            } catch(e) {
                console.error(e);
            }
        }
        totalSecs--;
    }, 1000);
}

function stopFocusLock() {
    if (confirm("Are you sure you want to exit your deep focus lock? Staying focused rewards maximum XP!")) {
        clearInterval(focusLockInterval);
        const overlay = document.getElementById('lockOverlay');
        if (overlay) overlay.style.display = 'none';
        showToast("Focus lock ended.");
    }
}

// =========================================================
// 11. TOAST NOTIFICATION UTILITY
// =========================================================
function showToast(message) {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}
