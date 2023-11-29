<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Insecure DjangoLab - README</title>
    <style>
        h1 {
            font-size: 36px;
        }
        h2 {
            font-size: 24px;
        }
        p, li {
            font-size: 16px;
        }
    </style>
</head>
<body>
    <h1>Insecure DjangoLab</h1>
    <h2>Instalasi</h2>
    <p>Untuk memulai menggunakan Insecure DjangoLab, ikuti langkah-langkah di bawah ini:</p>
    <ol>
        <li>Pastikan Anda telah menginstal Python pada sistem Anda. Aplikasi ini disarankan untuk menggunakan Python versi 3.8 atau yang lebih baru.</li>
        <li>Buat lingkungan virtual Python untuk mengisolasi paket-paket yang diperlukan. Buka terminal atau command prompt dan jalankan perintah berikut:
            <pre><code>python -m venv nama_lingkungan_virtual</code></pre>
        </li>
        <li>Aktifkan lingkungan virtual yang telah dibuat dengan perintah berikut:
            <ul>
                <li>Pada Windows:
                    <pre><code>nama_lingkungan_virtual\Scripts\activate</code></pre>
                </li>
                <li>Pada Unix atau MacOS:
                    <pre><code>source nama_lingkungan_virtual/bin/activate</code></pre>
                </li>
            </ul>
        </li>
        <li>Dengan lingkungan virtual aktif, instal Django dan library pendukung lainnya menggunakan file `requirements.txt` yang telah disediakan. Jalankan perintah:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>Setelah semua library terinstal, buat migrasi database dengan perintah:
            <pre><code>python manage.py makemigrations</code></pre>
            <pre><code>python manage.py migrate</code></pre>
        </li>
        <li>Anda kini dapat menjalankan server pengembangan Django dan mengakses aplikasi dengan:
            <pre><code>python manage.py runserver</code></pre>
        </li>
    </ol>

    <h2>Peringatan Keamanan</h2>
    <p>Aplikasi ini sengaja dibuat dengan kerentanan keamanan untuk keperluan pembelajaran. Jangan gunakan aplikasi ini dalam produksi atau di lingkungan yang dapat diakses publik. Selalu praktikkan pengembangan perangkat lunak dengan keamanan yang baik dan bertanggung jawab.</p>
</body>
</html>

