from brian2 import * #Kütüphanelerin tanımlanması
from numpy import * #Numeric python kütüphanesi temel matematiksel işlemlerin fonksiyonları
from matplotlib.pyplot import * #Grafik çizdirme için gerekli kütüphane

start_scope()
#Topla ve ateşle modelinin tanımlanması
#tau = 5*ms #tau değişkenine değer atama(Birimlere dikkat!)
a=-1
b=1
N=3 #hucre sayisi
# Çok satırlı ifadeleri yazmak için ''' kullanılır. Hücre denklemi bu şekilde tanımlanır.
eqs = ''' 
dv/dt = (a*v+b)/tau : 1
tau : second
'''
G = NeuronGroup(N, eqs, threshold='v>0.8', reset='v = 0', method='linear')
G.v='rand()'     #Baslangic kosulu
G.tau=[1*ms,10*ms,10*ms]
# Modeli gerçekleyen temel fonksiyon hücre sayısı, denklemi, çözüm metodu gibi değişkenlere sahiptir.
M = StateMonitor(G, 'v', record=True)
# Model çalıştırıldığında tüm veriler tutulmaz. StateMonitor gibi fonksiyonlarla kaydedilmek istenen değişkenler seçilir.

# Ateşlemelerin tutulmasını sağlayan fonksiyon.
spikemon = SpikeMonitor(G)

w=0.2 #sinaptik agirlik
S = Synapses(G, G,'w:1', on_pre='v_post += w') #Sinaps denklemi G'den G'ye presinaptik
#neuron ateşlediğinde post sinaptik neuronun v'si 0.2 artacak şekilde tanımlanmış.
S.connect(i=0, j=[1, 2])
S.w = 'j*0.2' # w hücrelerin indislerine bağlı olarak değiştirilmiş.
#Böylelikle ateşleme ile eklenen değerler hücreler arasında farklılık gösterecek.


run(30*ms)
# Model run komut ile belli bir süre işletilir. (Burada programın akışına dikkat!)

subplot(3,1,1)
plot(M.t/ms, M.v[0], 'k',label='Neuron 0')
ylabel('v')
legend()
subplot(3,1,2)
plot(M.t/ms, M.v[1], 'r',label='Neuron 1')
ylabel('v')
legend()
subplot(3,1,3)
plot(M.t/ms, M.v[2], 'b',label='Neuron 2')
xlabel('Time (ms)')
ylabel('v')
legend()
show()
