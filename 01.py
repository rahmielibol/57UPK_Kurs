from brian2 import * #Kütüphanelerin tanımlanması
from numpy import * #Numeric python kütüphanesi temel matematiksel işlemlerin fonksiyonları
from matplotlib.pyplot import * #Grafik çizdirme için gerekli kütüphane

#Topla ve ateşle modelinin tanımlanması
tau = 5*ms #tau değişkenine değer atama(Birimlere dikkat!)
a=-1
d=1
# Çok satırlı ifadeleri yazmak için ''' kullanılır. Hücre denklemi bu şekilde tanımlanır.
eqs = ''' 
dv/dt = (a*v+d)/tau : 1
'''
G = NeuronGroup(1, eqs, method='linear') 
#G.v=0.1     #Baslangic kosulu
# Modeli gerçekleyen temel fonksiyon hücre sayısı, denklemi, çözüm metodu gibi değişkenlere sahiptir.
M = StateMonitor(G, 'v', record=0)
# Model çalıştırıldığında tüm veriler tutulmaz. StateMonitor gibi fonksiyonlarla kaydedilmek istenen değişkenler seçilir.
run(30*ms)
# Model run komut ile belli bir süre işletilir. (Burada programın akışına dikkat!)

plot(M.t/ms, M.v[0])# Kaydedilen veri grafiğe çizdirilir.
xlabel('Time (ms)')
ylabel('v')
