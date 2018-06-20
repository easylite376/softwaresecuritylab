.class public Lcom/example/abhishektiwari/debugtest/MainActivity;
.super Landroid/support/v7/app/AppCompatActivity;
.source "MainActivity.java"


# instance fields
.field private b1:Landroid/widget/Button;


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 11
    invoke-direct {p0}, Landroid/support/v7/app/AppCompatActivity;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick_1(Landroid/view/View;)V
    .locals 6
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 24
    const-string v4, "TAG"

    const-string v5, "Inside onclik 1"

    invoke-static {v4, v5}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 25
    invoke-virtual {p0}, Lcom/example/abhishektiwari/debugtest/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v0

    .line 26
    .local v0, "context":Landroid/content/Context;
    const-string v2, "Inside onclik 1!"

    .line 27
    .local v2, "text":Ljava/lang/CharSequence;
    const/4 v1, 0x0

    .line 29
    .local v1, "duration":I
    invoke-static {v0, v2, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v3

    .line 30
    .local v3, "toast":Landroid/widget/Toast;
    invoke-virtual {v3}, Landroid/widget/Toast;->show()V

    .line 31
    return-void
.end method

.method public onClick_2(Landroid/view/View;)V
    .locals 6
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 34
    const-string v4, "TAG"

    const-string v5, "Inside onclik 1"

    invoke-static {v4, v5}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 35
    invoke-virtual {p0}, Lcom/example/abhishektiwari/debugtest/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v0

    .line 36
    .local v0, "context":Landroid/content/Context;
    const-string v2, "Inside onclik 2!"

    .line 37
    .local v2, "text":Ljava/lang/CharSequence;
    const/4 v1, 0x0

    .line 39
    .local v1, "duration":I
    invoke-static {v0, v2, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v3

    .line 40
    .local v3, "toast":Landroid/widget/Toast;
    invoke-virtual {v3}, Landroid/widget/Toast;->show()V

    .line 41
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 1
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .prologue
    .line 17
    invoke-super {p0, p1}, Landroid/support/v7/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 18
    const v0, 0x7f040019

    invoke-virtual {p0, v0}, Lcom/example/abhishektiwari/debugtest/MainActivity;->setContentView(I)V

    .line 20
    const v0, 0x7f0c0058

    invoke-virtual {p0, v0}, Lcom/example/abhishektiwari/debugtest/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lcom/example/abhishektiwari/debugtest/MainActivity;->b1:Landroid/widget/Button;

    .line 21
    return-void
.end method
