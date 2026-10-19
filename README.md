# Casino Mafia RPG 🎰🔫

New Star Soccer kariyer modundan esinlenen, Python ve Streamlit ile geliştirilmiş menü tabanlı bir karar RPG’si. Kumarhanede para kazan, yaşam giderlerini karşıla, mafya gruplarıyla mücadele et ve sosyal çevreni dikkatli kur.

## Çalıştırma

Python 3.10+ önerilir.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

Windows’ta sanal ortamı `.venv\Scripts\activate` ile etkinleştir. Oyun tarayıcıda açılır.

## Temel döngü

- Başlangıç: **$1.000, 100 can, 100 tokluk, seviye 1**.
- Kumarhane ve sokak işleri para kazandırır. Eylemler tokluğu azaltır; sıfır toklukta can kaybedersin.
- Marketten yiyecek al, envanterden tüket. Hastanede tam tedavi $1.500.
- $10.000’da mafya etkinleşir. Önemli eylemlerden sonra normal haraç ihtimali %15’tir.
- $25.000’da koruma binası açılır. Koruma başına $5.000; her koruma gelen hasarı 5 azaltır ve ölmez.
- $50.000’da çete binası açılır. Üye başına $3.000; üyeler çatışmada kaybedilebilir.
- Eylemler XP kazandırır. Seviye eşiği `seviye × 100 XP`.
- Can sıfırlanırsa veya mafya etkinken paran biterse oyun biter. Devam eden Blackjack elindeki bahis, el sonuçlanana kadar masada tutulur.

## 📱 Sosyal ve mafya grupları

**Sosyal $15.000’a ulaştığında kalıcı olarak açılır.** İlk bağlantı istekleri hemen gelir. Sonrakiler oyun eylemleriyle üretilir; ekranı yenilemek veya menülerde dolaşmak istek üretmez.

- İstekler ağırlıklı olarak kadın profillerinden ve sana saldıran mafyaların düşmanlarından gelir.
- Her yeni isteğin niyeti **%50 iyi / %50 kötü** olarak belirlenir. Mesajlar gerçek niyeti önceden açıklamaz.
- İyi niyetli bağlantıyı kabul etmek $150–500 destek ve stres azalması sağlar.
- Kötü niyetli bağlantıyı kabul etmek konumunu açığa çıkarır ve **normal haraçlara ek bir baskın** oluşturur. Reddetmek baskın oluşturmaz.
- İstek gelme ihtimali $15.000’da eylem başına %30, her ek $15.000’da +10 puan; üst sınır %85. Parti büyüklüğü 1’den 5’e yükselir. Bekleyen istek sınırı 30.
- Gruplar: **Karahan Ailesi (24), Kuzgunlar (18), Liman Kardeşliği (30)**.
- Grup yanındaki `x/x`, **sosyal ağına kabul ettiğin grup üyesi / toplam grup üyesi** sayısıdır. Her grubun ağa sızabilecek üye sayısı sınırlıdır.

## Kumarhane

### Rulet

Yeşil keçe masa, Avrupa sıralamasında tek sıfırlı 37 cepli çark, top ve animasyon. Fiş seçip masaya tıklayarak aynı turda birden fazla alana bahis koyabilirsin. Geri al ve temizleme desteklenir.

| Bahis | Net kazanç oranı |
| --- | --- |
| Tek sayı | 35:1 |
| Split (2 sayı) | 17:1 |
| Street / Trio (3 sayı) | 11:1 |
| Corner / İlk dört sayı | 8:1 |
| Six line (6 sayı) | 5:1 |
| Düzine / Sütun | 2:1 |
| Kırmızı–siyah / Tek–çift / 1–18–19–36 | 1:1 |

Kazanç ödemesine yatırılan bahis de eklenir. Örneğin $10 tek sayı bahsi tutarsa $360 toplam ödeme alınır. Sıfır, dış bahislerin tamamını kaybettirir. Split/corner için sayı kenarlarına ve kesişimlerine tıkla; six line ve sıfırlı kombinasyonlar için “Diğer bahisler” bölümünü kullan.

Oyunun akıcılığı için **%12 RPG şans desteği** vardır: bu turlarda bahislerin kapsadığı sayılardan biri seçilir; diğer turlarda 0–36 eşit olasılıklıdır. Bu, gerçek kumarhanenin olasılıklarını temsil etmez. Çoklu bahislerden birinin tutması, turun toplamda kârlı olacağını garanti etmez.

### Zar · Düşük / Yüksek

İki adet altı yüzlü zar atılır. Her tur değişen **3–11** hedefinin altında mı üstünde mi kalınacağını tahmin et. Hedef aralığı her iki seçimin de mümkün kalmasını sağlar; 2 ve 14 hiçbir zaman hedef olmaz. Toplam hedefe eşitse bahis iade edilir. Kazanma ödemesi toplam **2×** bahistir.

### Yazı Tura

Yazı ve tura eşit **%50** olasılıklıdır. Kazanma ödemesi toplam **2×** bahistir.
Sarı para her atışta **3 saniye** döner: yazı yüzünde **5 EURO**, tura yüzünde **Playboy tavşan logosu** bulunur. Sonuç ve ödeme dönüş tamamlandıktan sonra gösterilir.

### Blackjack

- Hit ve Stand; aslar 1 veya 11 değerinde sayılır.
- Kazançta toplam **2×** ödeme, eşitlikte bahis iadesi.
- **Double:** ilk iki kartta ek bahis yatırılır; elin bahsi ikiye katlanır ve oyuncu tek kart çeker. Bu oyunun özel kuralıyla krupiyer de yalnızca **bir ek kart** çeker.
- **Split:** aynı rank’taki iki kart iki ele ayrılır (ör. 8/8 veya K/K). İkinci el için ilk bahis kadar ek ücret alınır; eller ayrı oynanır ve ayrı sonuçlanır. Tur başına bir Split desteklenir; Split sonrası Double yapılabilir.
- Tüm eller aynı krupiyer eliyle karşılaştırılır. Herhangi bir elde Double yapıldıysa, tüm eller bittikten sonra krupiyere tek ek kart kuralı uygulanır; aksi halde krupiyer 17’ye kadar çeker.
- Sonuç yalnızca bir kez ödenir; sonuç ekranını tekrar görüntülemek ek para vermez.

At yarışı da mevcuttur; kazanan at için toplam ödeme 2× bahistir. Tüm casino oyunlarında minimum bahis $10’dur.

## Durum barları ve stres

Tüm ekranlarda para, can, tokluk, seviye/XP, koruma, çete ve stres görünür. Koruma barı 10 kişide dolar; ek korumaların etkisi sürer. Seviye barı sonraki seviyeye XP ilerlemesini gösterir.

Stres 0–100 aralığındadır: para harcama/kaybetme ve mafya baskınları artırır; para kazanma, destekçiler, koruma ve çete alımı azaltır. **Yalnızca görseldir; kararları, hasarı veya kazanma olasılıklarını etkilemez.**

## Kayıt

Ana menüde Save/Load düğmeleriyle `savegame.json` kullanılır. Oyuncu, stres, envanter, sosyal istekler/bağlantılar, gruplar ve bekleyen baskınlar kaydedilir. Önceki sürüm kayıtları yeni alanlara varsayılan değerler verilerek yüklenir.

## Dosyalar

- `main.py`: sayfalar ve ana oyun akışı
- `player.py`, `game_state.py`: oyuncu ve oturum durumu
- `social.py`, `mafia.py`: bağlantılar, gruplar, baskınlar ve çatışma
- `ui_components.py`: ortak durum barları ve arayüz yardımcıları
- `casino/`: Blackjack, rulet, zar, yazı tura ve at yarışı
- `casino/roulette_frontend/index.html`: etkileşimli rulet masası ve SVG çark
- `market.py`, `hospital.py`, `secure.py`, `gang.py`, `inventory.py`: ihtiyaçlar ve ilerleme
- `save_load.py`: JSON kayıt ve eski kayıtların uyarlanması
- `tests/`: para, olasılık kuralları, sosyal baskınlar ve kayıt regresyon testleri

## Test

```bash
python -m unittest discover -s tests -v
```
