from brian2 import * #Kütüphanelerin tanımlanması
from numpy import * #Numeric python kütüphanesi temel matematiksel işlemlerin fonksiyonları
from matplotlib.pyplot import * #Grafik çizdirme için gerekli kütüphane

start_scope()
#Topla ve ateşle modelinin tanımlanması
tau = 5*ms #tau değişkenine değer atama(Birimlere dikkat!)
a=-1
b=1
# Çok satırlı ifadeleri yazmak için ''' kullanılır. Hücre denklemi bu şekilde tanımlanır.
eqs = ''' 
dv/dt = (a*v+b)/tau : 1
'''
G = NeuronGroup(1, eqs, threshold='v>0.8', reset='v = 0', method='linear')
#G.v=0.1     #Baslangic kosulu
# Modeli gerçekleyen temel fonksiyon hücre sayısı, denklemi, çözüm metodu gibi değişkenlere sahiptir.
M = StateMonitor(G, 'v', record=0)
# Model çalıştırıldığında tüm veriler tutulmaz. StateMonitor gibi fonksiyonlarla kaydedilmek istenen değişkenler seçilir.

# Ateşlemelerin tutulmasını sağlayan fonksiyon.
spikemon = SpikeMonitor(G)


run(30*ms)
# Model run komut ile belli bir süre işletilir. (Burada programın akışına dikkat!)

plot(M.t/ms, M.v[0])# Kaydedilen veri grafiğe çizdirilir.
for t in spikemon.t: #t spikemon.t dizisinin içindeki değerleri sırasıyla alacak
    axvline(t/ms, ls='--', c='r', lw=3) #Dikine çizgi çizdirir.
xlabel('Time (ms)')
ylabel('v');
show()

#Atesleme zamanlari
for t in spikemon.t:
    print(t)