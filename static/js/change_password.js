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
        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }
        document.addEventListener('DOMContentLoaded', () => {
            const flashMessages = document.querySelectorAll('.flash-message');
            flashMessages.forEach(msg => {
                let type = msg.classList.contains('success') ? 'success' : 'error';
                showToast(msg.textContent, type);
                msg.remove();
            });
        });
