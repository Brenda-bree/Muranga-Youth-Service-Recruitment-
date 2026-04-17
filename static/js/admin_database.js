        function showToast(message, type) {
            const container = document.getElementById('toastContainer');
            if (!container) return;
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            let icon = type === 'success' ? '<i class="fas fa-check-circle"></i>' : '<i class="fas fa-exclamation-circle"></i>';
            toast.innerHTML = `${icon}<div class="toast-content">${escapeHtml(message)}</div><button class="toast-close">&times;</button>`;
            container.appendChild(toast);
            toast.querySelector('.toast-close').onclick = () => toast.remove();
            setTimeout(() => toast.remove(), 5000);
        }

        function customConfirm(message) {
            return new Promise((resolve) => {
                let modal = document.getElementById('customConfirmModal');
                if (!modal) {
                    modal = document.createElement('div');
                    modal.id = 'customConfirmModal';
                    modal.className = 'modal-overlay';
                    modal.innerHTML = `
                        <div class="confirm-modal">
                            <div class="confirm-modal-header"><h3><i class="fas fa-exclamation-triangle"></i> Confirm Action</h3></div>
                            <div class="confirm-modal-body"><p id="confirmMessage"></p></div>
                            <div class="confirm-modal-footer">
                                <button class="confirm-cancel" id="confirmNo">Cancel</button>
                                <button class="confirm-confirm" id="confirmYes">Delete</button>
                            </div>
                        </div>`;
                    document.body.appendChild(modal);
                }
                const messageSpan = document.getElementById('confirmMessage');
                const confirmBtn = document.getElementById('confirmYes');
                const cancelBtn = document.getElementById('confirmNo');
                messageSpan.textContent = message;
                modal.classList.add('active');
                const cleanup = () => {
                    modal.classList.remove('active');
                    confirmBtn.removeEventListener('click', handleConfirm);
                    cancelBtn.removeEventListener('click', handleCancel);
                };
                const handleConfirm = () => { cleanup(); resolve(true); };
                const handleCancel = () => { cleanup(); resolve(false); };
                confirmBtn.addEventListener('click', handleConfirm);
                cancelBtn.addEventListener('click', handleCancel);
            });
        }

        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.preventDefault();
                const confirmed = await customConfirm('Delete this recruitee? This action cannot be undone.');
                if (confirmed) window.location.href = btn.href;
            });
        });

        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }

        // Convert flash messages to toasts
        document.addEventListener('DOMContentLoaded', () => {
            const flashMessages = document.querySelectorAll('.flash-message');
            flashMessages.forEach(msg => {
                let type = 'info';
                if (msg.classList.contains('success')) type = 'success';
                else if (msg.classList.contains('error')) type = 'error';
                showToast(msg.textContent, type);
                msg.remove();
            });
        });
