"""Action-driven social requests with hidden allegiances and independent raids."""
import random
import streamlit as st
from game_state import get_player, navigate_to

UNLOCK_AMOUNT = 15000
WOMEN = ['Elif', 'Defne', 'Zeynep', 'Maya', 'Selin', 'Derya', 'Ece', 'Lara']
ALLIES = ['Bora', 'Kaan', 'Deniz', 'Aras', 'Eren']


def request_rate(money):
    """Higher wealth increases both request probability and batch size."""
    tier = max(0, (money - UNLOCK_AMOUNT) // 15000)
    return min(0.85, 0.30 + tier * 0.10), min(5, 1 + tier)


def generate_request():
    state = st.session_state
    known = state.social_requests + state.social_contacts
    available = [group for group in state.mafia_groups if sum(
        r.get('group_id') == group['id'] for r in known) < group['total']]
    # Exactly half of new requests are hostile; do not replace exhausted spies
    # with friendly requests, which would silently change the probability.
    hostile = random.random() < 0.5
    if hostile and not available:
        return None
    group = random.choice(available if hostile else state.mafia_groups)
    woman = random.random() < 0.75
    request = {
        'id': state.social_next_id,
        'name': random.choice(WOMEN if woman else ALLIES),
        'avatar': '👩' if woman else '🧑',
        'bio': random.choice([
            'Zor günlerinde yanında olmak isterim.',
            'Başına gelenleri duydum. Yalnız değilsin.',
            'Ortak düşmanlarımız var. Birbirimize destek olabiliriz.',
            'Şehirde yeni dostlara ihtiyacımız var.',
        ]),
        'hostile': hostile,
        'group_id': group['id'] if hostile else None,
        'enemy_of': None if hostile else group['id'],
        'revealed': False,
    }
    state.social_next_id += 1
    return request


def add_requests(count):
    for _ in range(min(count, max(0, 30 - len(st.session_state.social_requests)))):
        request = generate_request()
        if request:
            st.session_state.social_requests.append(request)


def update_social():
    """Called each render; only real actions generate additional requests."""
    player = get_player()
    state = st.session_state
    if not state.social_unlocked and player.money >= UNLOCK_AMOUNT:
        state.social_unlocked = True
        state.social_last_action = player.total_actions
        add_requests(request_rate(player.money)[1])
        st.toast('📱 Sosyal açıldı! Yeni bağlantı isteklerin var.')
    if not state.social_unlocked:
        state.social_last_action = player.total_actions
        return
    actions = max(0, player.total_actions - state.social_last_action)
    state.social_last_action = player.total_actions
    probability, batch = request_rate(player.money)
    for _ in range(actions):
        if random.random() < probability:
            add_requests(batch)


def accept_request(request_id):
    state = st.session_state
    request = next((r for r in state.social_requests if r['id'] == request_id), None)
    if request is None:
        return
    state.social_requests.remove(request)
    state.social_contacts.append(request)
    player = get_player()
    if request['hostile']:
        # Never replaces or rolls against the ordinary 15% extortion check.
        state.social_raids.append({'group_id': request['group_id'], 'contact_id': request['id']})
    else:
        gift = random.randint(150, 500)
        player.add_money(gift)
        player.change_stress(-8)
        request['revealed'] = True
        request['gift'] = gift
        state.social_notice = f"{request['name']} sana ${gift:,} destek gönderdi."


def group_contact_count(group_id):
    return sum(c.get('group_id') == group_id for c in st.session_state.social_contacts)


def render_mafia_groups():
    st.markdown('### 🔫 Mafya grupları')
    st.caption('x/x = sosyal ağında seni ekleyen ve kabul ettiğin grup üyesi / grubun toplam üyesi. Kimlikler istek sırasında gizlidir.')
    for group in st.session_state.mafia_groups:
        count = group_contact_count(group['id'])
        st.markdown(f"**{group['name']} · {count}/{group['total']}**")
        st.progress(min(1.0, count / group['total']))


def render_social():
    st.markdown('## 📱 Sosyal')
    if not st.session_state.social_unlocked:
        st.info('🔒 Sosyal ağ $15.000 birikime ulaştığında açılır.')
    else:
        st.caption('İsteklerin %50’si iyi, %50’si kötü niyetlidir. Kabul ettiğin bir casus konumunu mafyaya gönderebilir. Servetin arttıkça istekler sıklaşır.')
        if st.session_state.get('social_notice'):
            st.success(st.session_state.pop('social_notice'))
        requests, contacts = st.tabs([
            f"İstekler ({len(st.session_state.social_requests)})",
            f"Bağlantılar ({len(st.session_state.social_contacts)})",
        ])
        with requests:
            if not st.session_state.social_requests:
                st.info('Şimdilik yeni istek yok. Oynamaya devam ettikçe yeni istekler gelecek.')
            for request in list(st.session_state.social_requests):
                with st.container(border=True):
                    st.markdown(f"### {request['avatar']} {request['name']} · #{request['id']}")
                    st.write(request['bio'])
                    yes, no = st.columns(2)
                    if yes.button('Kabul et', key=f"accept_{request['id']}", use_container_width=True):
                        accept_request(request['id'])
                        st.rerun()
                    if no.button('Reddet', key=f"decline_{request['id']}", use_container_width=True):
                        st.session_state.social_requests.remove(request)
                        st.rerun()
        with contacts:
            for contact in st.session_state.social_contacts:
                status = 'Bağlantı kuruldu · kimlik bilinmiyor'
                if contact['revealed']:
                    status = '🚨 Mafya casusu · konumunu paylaştı' if contact['hostile'] else f"💚 Destekçi · ${contact.get('gift', 0):,} yardım"
                st.write(f"{contact['avatar']} **{contact['name']}** · {status}")
            if not st.session_state.social_contacts:
                st.info('Henüz bağlantın yok.')
    render_mafia_groups()
    if st.button('🏠 Ana menü', key='social_back', use_container_width=True):
        navigate_to('main_menu')
