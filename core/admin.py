from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Produto, Servico, Agendamento, Avaliacao, Contato


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'produtos_count', 'servicos_count', 'criado_em']
    search_fields = ['nome']
    ordering = ['nome']
    
    def produtos_count(self, obj):
        return obj.produtos.count()
    produtos_count.short_description = 'Produtos'
    
    def servicos_count(self, obj):
        return obj.servicos.count()
    servicos_count.short_description = 'Serviços'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'categoria',
        'preco_formatado',
        'estoque_status',
        'marca',
        'codigo_sku',
        'ativo',
        'criado_em'
    ]
    list_filter = ['categoria', 'ativo', 'criado_em']
    search_fields = ['nome', 'codigo_sku', 'marca', 'compatibilidade']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'categoria', 'codigo_sku')
        }),
        ('Preço e Estoque', {
            'fields': ('preco', 'estoque')
        }),
        ('Detalhes do Produto', {
            'fields': ('marca', 'compatibilidade', 'peso', 'garantia', 'imagem')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def preco_formatado(self, obj):
        return f"R$ {obj.preco:.2f}"
    preco_formatado.short_description = 'Preço'
    
    def estoque_status(self, obj):
        if obj.estoque > 20:
            color = 'green'
            status = '✓ Em Estoque'
        elif obj.estoque > 0:
            color = 'orange'
            status = '⚠ Pouco Estoque'
        else:
            color = 'red'
            status = '✗ Sem Estoque'
        return format_html(f'<span style="color: {color};"><b>{status}</b> ({obj.estoque})</span>')
    estoque_status.short_description = 'Estoque'


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'categoria',
        'preco_formatado',
        'duracao_formatada',
        'avaliacoes_count',
        'ativo',
        'criado_em'
    ]
    list_filter = ['categoria', 'ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'categoria')
        }),
        ('Preço e Duração', {
            'fields': ('preco', 'duracao_estimada')
        }),
        ('Mídia', {
            'fields': ('imagem',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def preco_formatado(self, obj):
        return f"R$ {obj.preco:.2f}"
    preco_formatado.short_description = 'Preço'
    
    def duracao_formatada(self, obj):
        duracao = obj.duracao_estimada
        if duracao < 60:
            return f"{duracao}min"
        else:
            horas = duracao // 60
            minutos = duracao % 60
            if minutos == 0:
                return f"{horas}h"
            return f"{horas}h{minutos}min"
    duracao_formatada.short_description = 'Duração'
    
    def avaliacoes_count(self, obj):
        return obj.avaliacoes.count()
    avaliacoes_count.short_description = 'Avaliações'


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'usuario',
        'servico',
        'data_agendamento_formatada',
        'status_badge',
        'nome_cliente',
        'telefone_cliente'
    ]
    list_filter = ['status', 'data_agendamento', 'criado_em', 'servico__categoria']
    search_fields = ['usuario__username', 'nome_cliente', 'telefone_cliente', 'veiculo']
    readonly_fields = ['criado_em', 'atualizado_em', 'usuario']
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('usuario',)
        }),
        ('Serviço', {
            'fields': ('servico', 'data_agendamento')
        }),
        ('Dados do Cliente', {
            'fields': ('nome_cliente', 'email_cliente', 'telefone_cliente')
        }),
        ('Veículo', {
            'fields': ('veiculo', 'placa_veiculo')
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def data_agendamento_formatada(self, obj):
        return obj.data_agendamento.strftime('%d/%m/%Y %H:%M')
    data_agendamento_formatada.short_description = 'Data/Hora'
    
    def status_badge(self, obj):
        colors = {
            'pendente': '#FFA500',
            'confirmado': '#4CAF50',
            'em_progresso': '#2196F3',
            'concluido': '#8BC34A',
            'cancelado': '#F44336',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            f'<span style="background-color: {color}; color: white; padding: 3px 10px; border-radius: 3px;">{obj.get_status_display()}</span>'
        )
    status_badge.short_description = 'Status'


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'servico',
        'rating_stars',
        'agendamento',
        'criado_em'
    ]
    list_filter = ['rating', 'criado_em', 'servico__categoria']
    search_fields = ['usuario__username', 'servico__nome', 'comentario']
    readonly_fields = ['criado_em', 'usuario', 'agendamento']
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return stars
    rating_stars.short_description = 'Rating'


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'email',
        'assunto',
        'lido_status',
        'criado_em'
    ]
    list_filter = ['lido', 'criado_em']
    search_fields = ['nome', 'email', 'assunto', 'mensagem']
    readonly_fields = ['criado_em', 'nome', 'email', 'telefone', 'assunto', 'mensagem']
    
    fieldsets = (
        ('Contato do Cliente', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Mensagem', {
            'fields': ('assunto', 'mensagem')
        }),
        ('Status', {
            'fields': ('lido',)
        }),
        ('Data', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )
    
    def lido_status(self, obj):
        if obj.lido:
            return format_html('<span style="color: green;">✓ Lido</span>')
        return format_html('<span style="color: red;">✗ Não Lido</span>')
    lido_status.short_description = 'Status'
